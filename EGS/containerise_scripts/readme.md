# Containerise Scripts

This folder contains scripts to help containerize PyTorch applications with GPU support. Below is a brief overview of the scripts and their functionalities.

## Files

### `dockerize.py`

This script automates the process of creating a Docker image for a PyTorch script. It includes the following functionalities:

- Extracts dependencies from the PyTorch script and generates a `requirements.txt` file.
- Generates a `Dockerfile` with the required dependencies and GPU support.
- Creates a Docker image from the given PyTorch script.

#### Usage

```sh
python dockerize.py <script_path>
```
