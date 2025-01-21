import os
import argparse
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset

# Dummy Dataset
class DummyDataset(Dataset):
    def __init__(self, size=1000, features=10):
        self.data = torch.randn(size, features)
        self.labels = torch.randint(0, 2, (size,))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index], self.labels[index]

# Simple Model
class SimpleModel(nn.Module):
    def __init__(self, input_size=10, output_size=2):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(input_size, output_size)

    def forward(self, x):
        return self.fc(x)

def train(rank, world_size, dataset, epochs=5, batch_size=32):
    dist.init_process_group("nccl", rank=rank, world_size=world_size)

    # Set device
    device = torch.device(f"cuda:{rank}" if torch.cuda.is_available() else "cpu")

    # Split dataset
    worker_split = len(dataset) // world_size
    start_idx = rank * worker_split
    end_idx = start_idx + worker_split
    local_dataset = torch.utils.data.Subset(dataset, range(start_idx, end_idx))
    dataloader = DataLoader(local_dataset, batch_size=batch_size, shuffle=True)

    # Model and optimizer
    model = SimpleModel()
    model = model.to(device)
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss()

    # Training loop
    for epoch in range(epochs):
        for data, target in dataloader:
            data, target = data.to(device), target.to(device)

            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()

            # Gradient synchronization
            for param in model.parameters():
                dist.all_reduce(param.grad.data, op=dist.ReduceOp.SUM)
                param.grad.data /= world_size

            optimizer.step()

        if rank == 0:
            print(f"Epoch {epoch}, Loss: {loss.item()}")

    dist.destroy_process_group()

def main():
    # Get rank and world size from environment variables
    rank = int(os.environ["RANK"])
    world_size = int(os.environ["WORLD_SIZE"])
    master_addr = os.environ["MASTER_ADDR"]
    master_port = os.environ["MASTER_PORT"]

    # Dummy dataset
    dataset = DummyDataset(size=1000, features=10)

    # Train the model
    train(rank, world_size, dataset)

if __name__ == "__main__":
    main()
