import egs
import subprocess
import time
import json
import requests

def ask_to_continue(step):
    response = input(f"Do you want to continue to the next step: {step}? (yes/no): ")
    if response.lower() != "yes":
        print("Exiting script.")
        exit()


# Step 1: Authenticate with EGS using the user's API key
def authenticate(ENDPOINT, API_KEY):
    # ask_to_continue("Authenticate with EGS")
    print("Authenticating with EGS...")
    auth = egs.authenticate(endpoint=ENDPOINT, api_key=API_KEY)
    print("Authentication successful.")
    return auth

# Step 2: Create manual GPR requests for slices
def create_gpr_requests(auth, workspace_name, slices, CLUSTER_NAME):
    # ask_to_continue("Create GPR requests")
    for request_name, priority in slices.items():
        for i in range(1):
            print(f"Creating GPR request {request_name}_{i+1} for request '{request_name}' with priority '{priority}'...")

            inventory = egs.inventory(authenticated_session=auth).__str__()
            # convert string to json
            inventory = json.loads(inventory)
            print(f"Inventory retrieved successfully.")
            
            print(json.dumps(inventory, indent=4))

            print(inventory["managed_nodes"][0]["memory"], inventory["managed_nodes"][0]["instance_type"], inventory["managed_nodes"][0]["gpu_shape"])
            # print all the inventory items that are used in the GPR request
            print(inventory["managed_nodes"][0]["memory"], inventory["managed_nodes"][0]["instance_type"], inventory["managed_nodes"][0]["gpu_shape"])

            request_name = f"{request_name}_{i+1}"
            gpu_request_id = egs.request_gpu(request_name=request_name, workspace_name=workspace_name, cluster_name=CLUSTER_NAME[0], node_count=1, gpu_per_node_count=1, memory_per_gpu=int(inventory["managed_nodes"][0]["memory"]), instance_type=inventory["managed_nodes"][0]["instance_type"], gpu_shape=inventory["managed_nodes"][0]["gpu_shape"], exit_duration="0d0h3m", priority=priority, authenticated_session=auth)

            print(f"GPR request {request_name}_{i+1} created successfully with GPU request ID '{gpu_request_id}'.")

            print(f"Waiting for 10 seconds before creating the next GPR request...")
            time.sleep(10)  # To avoid overwhelming the API


# def delete_gpr_requests(auth, workspace_name):
#     # ask_to_continue("Delete GPR requests")
#     gpr_list = egs.gpu_request_status_for_workspace(workspace_name, authenticated_session=auth)
#     for gpr in gpr_list["items"]



def main():
    # take the config.json file as an argument
    import sys
    print(len(sys.argv))
    if len(sys.argv) != 2:
        print("Usage: python user_script.py <config.json>")
        exit(1)

    # get the config file
    config_file = sys.argv[1]

    # Load configuration from JSON file
    def load_config(file_path=config_file):
        with open(file_path, "r") as file:
            return json.load(file)

    # Load the configuration
    config_data = load_config()

    # Iterate over each team's configuration
    for team, config in config_data.items():
        print(f"\nProcessing configuration for team: {team}")

        # Extract values for the current team
        ENDPOINT = config["ENDPOINT"]
        WORKSPACE_NAME = config["WORKSPACE_NAME"]
        CLUSTER_NAME = config["CLUSTER_NAME"]

        # Read user api key from user folder
        with open(f"./{team}/api-token.txt", "r") as file:
            USER_API_KEY = file.read().strip()

        # Placeholder for any further processing per team
        print(f"Completed processing API-Token for team: {team}\n{'='*50}")

        user_auth = authenticate(ENDPOINT=ENDPOINT, API_KEY=USER_API_KEY)

        # Define slices and their GPU shapes
        slices = {
            "low priority": 1,
            "important fine tuning": 101,
            "EMERGENCY": 201
        }

        print("Installing GPU workloads...")

        subprocess.run(["kubectl", "--kubeconfig", f"./{team}/{team}-kubeconfig.yaml", "apply", "-f", f"./llm-deployment.yaml"], check=True)

        subprocess.run(["kubectl", "--kubeconfig", f"./{team}/{team}-kubeconfig.yaml", "apply", "-f", f"./service.yaml"], check=True)

        # # sleep for 60 seconds
        # print("Waiting for 60 seconds ...")
        # time.sleep(60)

        # kubectl get svc and get the external ip

        # # Create load against the service
        # print("Creating load against the service...")
        # external_ip = print(subprocess.run(["kubectl", "get", "svc", "llm-service", "-o", "jsonpath={.status.loadBalancer.ingress[0].hostname}"], capture_output=True, text=True, check=True).stdout.strip())

        # url = f"http://{external_ip}/generate"
        # headers = {"Content-Type": "application/json"}
        # data = {"input": "What is Kubernetes?"}

        # for _ in range(3600):
        #     try:
        #         response = requests.post(url, json=data, headers=headers)
        #         print(f"Response: {response.status_code}, {response.text}")
        #     except requests.RequestException as e:
        #         print(f"Error: {e}")
        #     time.sleep(1)

        print("Creating GPR requests...")
        # Create GPR requests for each slice
        create_gpr_requests(user_auth, WORKSPACE_NAME, slices, CLUSTER_NAME)
        
        print("GPU workload automation script completed successfully.")
        # delete_gpr_requests(user_auth, WORKSPACE_NAME)

if __name__ == "__main__":
    main()
