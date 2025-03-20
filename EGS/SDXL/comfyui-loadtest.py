import json
import time
import uuid
import logging
from urllib import request, error
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from tqdm import tqdm
import random
import base64


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
API_ENDPOINT = "http://132.226.47.15/prompt"
RATE_PER_SECOND = 5
DURATION_MINUTES = 1
IMAGE_DIR = "./image_sdxl"
REQUEST_TIMEOUT = 30  # Seconds

# Create image directory
os.makedirs(IMAGE_DIR, exist_ok=True)

# Base prompt template
PROMPT_TEMPLATE = json.loads("""
{
  "3": {
    "inputs": {
      "seed": 785878925762048,
      "steps": 20,
      "cfg": 8,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1,
      "model": ["4", 0],
      "positive": ["6", 0],
      "negative": ["7", 0],
      "latent_image": ["5", 0]
    },
    "class_type": "KSampler"
  },
  "4": {
    "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"},
    "class_type": "CheckpointLoaderSimple"
  },
  "5": {
    "inputs": {"width": 512, "height": 512, "batch_size": 2},
    "class_type": "EmptyLatentImage"
  },
  "6": {
    "inputs": {"text": "{PROMPT_TEXT}", "clip": ["4", 1]},
    "class_type": "CLIPTextEncode"
  },
  "7": {
    "inputs": {"text": "text, watermark", "clip": ["4", 1]},
    "class_type": "CLIPTextEncode"
  },
  "8": {
    "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
    "class_type": "VAEDecode"
  },
  "9": {
    "inputs": {"filename_prefix": "ComfyUI", "images": ["8", 0]},
    "class_type": "SaveImage"
  }
}
""")

def generate_prompt_variant(base_prompt):
    """Generate a unique prompt variant with random seed and prompt text"""
    variant = json.loads(json.dumps(base_prompt))
    variant["3"]["inputs"]["seed"] = int(time.time() * 1000) % 1000000000
    variant["6"]["inputs"]["text"] = random_prompt_text()
    return variant

def random_prompt_text():
    """Generate random prompt text combinations"""
    styles = ["surreal", "realistic", "impressionist", "cyberpunk", "steampunk"]
    subjects = ["landscape", "portrait", "still life", "abstract composition", "fantasy scene"]
    descriptors = ["intricate details", "dramatic lighting", "4k resolution", 
                  "unreal engine", "trending on artstation"]
    
    return f"A {random.choice(styles)} {random.choice(subjects)} with {random.choice(descriptors)}"

def send_request(prompt):
    """Send request to inference endpoint and save resulting image"""
    request_id = str(uuid.uuid4())[:8]
    filename = f"{int(time.time())}_{request_id}.png"
    filepath = os.path.join(IMAGE_DIR, filename)
    
    try:
        # Serialize and send request
        data = json.dumps({"prompt": prompt}).encode('utf-8')
        req = request.Request(API_ENDPOINT, data=data, method='POST')
        
        with request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            if response.status == 200:
                response_data = json.loads(response.read().decode('utf-8'))
                print(response_data)
                # Check if 'images' key exists in the response
                if 'images' in response_data and response_data['images']:
                    # Decode the base64 image data
                    image_data = base64.b64decode(response_data['images'][0])
                    
                    # Save the image
                    with open(filepath, 'wb') as f:
                        f.write(image_data)
                    logging.info(f"Saved image: {filename}")
                    return True
                else:
                    logging.error(f"No image data in response for request {request_id}")
                    return False
            else:
                logging.error(f"Request {request_id} failed with status: {response.status}")
                return False
                
    except error.HTTPError as e:
        logging.error(f"HTTP error {e.code} for request {request_id}: {e.reason}")
    except error.URLError as e:
        logging.error(f"URL error for request {request_id}: {e.reason}")
    except Exception as e:
        logging.error(f"Unexpected error for request {request_id}: {str(e)}")
        
    return False

def run_load_test():
    """Main load test execution"""
    total_requests = RATE_PER_SECOND * 60 * DURATION_MINUTES
    logging.info(f"Starting load test: {RATE_PER_SECOND}req/s for {DURATION_MINUTES} mins (~{total_requests} requests)")
    
    with ThreadPoolExecutor(max_workers=RATE_PER_SECOND * 2) as executor:
        futures = []
        start_time = time.time()
        
        # Progress bar setup
        with tqdm(total=total_requests, desc="Generating images", unit="img") as pbar:
            # Rate-controlled submission loop
            while (time.time() - start_time) < (DURATION_MINUTES * 60):
                batch_start = time.time()
                
                # Submit batch of requests
                for _ in range(RATE_PER_SECOND):
                    prompt = generate_prompt_variant(PROMPT_TEMPLATE)
                    futures.append(executor.submit(send_request, prompt))
                
                # Progress update
                completed = sum(future.done() for future in futures)
                pbar.update(completed - pbar.n)
                
                # Rate control
                elapsed = time.time() - batch_start
                if elapsed < 1:
                    time.sleep(1 - elapsed)
                    
            # Process remaining futures
            for future in as_completed(futures):
                pbar.update(1)

    logging.info(f"Load test completed. Images saved to: {IMAGE_DIR}")

if __name__ == "__main__":
    run_load_test()
