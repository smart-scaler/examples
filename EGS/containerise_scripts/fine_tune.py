import os
import json
import boto3
from torchtune import Trainer
from huggingface_hub import HfApi

# Environment variables
BUCKET_NAME = os.environ["BUCKET_NAME"]
CHUNK_DATA = json.loads(os.environ["CHUNK_DATA"])

# Initialize AWS client
s3 = boto3.client("s3")

# Download files from S3
def download_files(chunk, s3_client):
    files = []
    for file in chunk:
        key = file["Key"]
        local_path = key.split("/")[-1]  # Save file in the current directory
        s3_client.download_file(BUCKET_NAME, key, local_path)
        files.append(local_path)
    return files

# Fine-tune the model
def fine_tune_model(data_files):
    trainer = Trainer("your-llm-model")  # Replace with your Hugging Face model
    trainer.add_data(data_files)
    trainer.train()
    trainer.save("fine_tuned_model")
    return "fine_tuned_model"

# Publish the model to Hugging Face
def upload_model_to_hf(model_path):
    hf_api = HfApi()
    hf_api.upload_folder(model_path, repo_id="your-hf-repo")  # Replace with your Hugging Face repo

if __name__ == "__main__":
    print("Starting Worker...")
    data_files = download_files(CHUNK_DATA, s3)
    print(f"Downloaded {len(data_files)} files.")
    model_path = fine_tune_model(data_files)
    print(f"Model fine-tuned and saved at {model_path}.")
    upload_model_to_hf(model_path)
    print("Model published to Hugging Face.")