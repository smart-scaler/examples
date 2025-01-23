import os
import argparse
import shutil
import subprocess
import ast
import pkg_resources

def extract_dependencies(script_path):
    """Extracts import statements from the script and generates a requirements.txt file."""
    dependencies = set()
    try:
        with open(script_path, "r") as script_file:
            tree = ast.parse(script_file.read(), filename=script_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        dependencies.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    dependencies.add(node.module.split(".")[0])

        # Filter out standard library modules (basic heuristic)
        std_libs = {"os", "sys", "shutil", "subprocess", "argparse", "ast"}
        dependencies = dependencies - std_libs

        # Resolve child dependencies using pip
        resolved_dependencies = set()
        for dep in dependencies:
            try:
                dist = pkg_resources.get_distribution(dep)
                resolved_dependencies.add(f"{dist.project_name}=={dist.version}")
            except pkg_resources.DistributionNotFound:
                resolved_dependencies.add(dep)  # Fallback to unversioned dependency

        # Write to requirements.txt
        if resolved_dependencies:
            with open("requirements.txt", "w") as req_file:
                req_file.write("\n".join(resolved_dependencies))
                print("requirements.txt created with dependencies:", resolved_dependencies)
        else:
            print("No external dependencies found.")

    except Exception as e:
        print(f"Error extracting dependencies: {e}")

def generate_dockerfile(script_name, base_image="nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04"):
    """Generates a Dockerfile with the required dependencies and GPU support."""
    dockerfile_content = f"""
    FROM {base_image}

    # Install system dependencies
    RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        python3-dev \
        git && \
        apt-get clean && rm -rf /var/lib/apt/lists/*

    # Install NVIDIA PyTorch dependencies
    RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

    # Set the working directory
    WORKDIR /app

    # Copy the PyTorch script into the container
    COPY {script_name} /app/{script_name}

    # Install Python dependencies (if a requirements.txt exists)
    COPY requirements.txt /app/requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt || echo "No requirements.txt found"

    # Set the default command to run the script
    CMD ["python3", "{script_name}"]
    """
    return dockerfile_content

def create_docker_image(script_path, image_name):
    """Creates a Docker image from the given PyTorch script."""
    script_name = os.path.basename(script_path)
    script_dir = os.path.dirname(script_path)

    # Create a temporary build directory
    build_dir = os.path.join(script_dir, "docker_build")
    os.makedirs(build_dir, exist_ok=True)

    try:
        # Extract dependencies and create requirements.txt
        extract_dependencies(script_path)

        # Copy the script to the build directory
        shutil.copy(script_path, os.path.join(build_dir, script_name))

        # Check if requirements.txt exists and copy it
        requirements_path = os.path.join(script_dir, "requirements.txt")
        if os.path.exists(requirements_path):
            shutil.copy(requirements_path, os.path.join(build_dir, "requirements.txt"))

        # Generate and write the Dockerfile
        dockerfile_content = generate_dockerfile(script_name)
        dockerfile_path = os.path.join(script_dir, "Dockerfile")
        print("Dockerfile path:", dockerfile_path)
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)

    except Exception as e:
        print(f"Error creating Docker image: {e}")

    finally:
        # Clean up the temporary build directory
        shutil.rmtree(build_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Docker image for a PyTorch script with GPU support.")
    parser.add_argument("script", help="Path to the PyTorch script.")
    parser.add_argument("--image-name", default="pytorch_script_image", help="Name of the Docker image.")
    args = parser.parse_args()

    create_docker_image(args.script, args.image_name)
