import egs
import subprocess
import time
import json
import base64

def ask_to_continue(step):
    response = input(f"Do you want to continue to the next step: {step}? (yes/no): ")
    if response.lower() != "yes":
        print("Exiting script.")
        exit()

import json

# Step 1: Authenticate with EGS
def authenticate(ENDPOINT, API_KEY):
    # ask_to_continue("Authenticate with EGS")
    print("Authenticating with EGS...")
    auth = egs.authenticate(endpoint=ENDPOINT, api_key=API_KEY)
    print("Authentication successful.")
    return auth


# Step 2: Create workspace and associate it with the namespace
def create_workspace(auth, workspace_name, namespace, CLUSTER_NAME, USER_NAME, USER_EMAIL):
    # ask_to_continue("Create workspace ")
    print(f"Creating workspace '{workspace_name}' and associating it with namespace '{namespace}'...")
    workspace = egs.create_workspace(workspace_name, clusters=CLUSTER_NAME, namespaces=namespace, username=USER_NAME, email=USER_EMAIL, authenticated_session=auth)
    print(f"Workspace '{workspace_name}' created successfully.")
    return workspace


def Delete_workspace(auth, workspace_name):
    # ask_to_continue("Deleting workspace {workspace_name}")
    print(f"Deleting workspace '{workspace_name}'")
    workspace = egs.delete_workspace(workspace_name, authenticated_session=auth)
    print(f"Workspace '{workspace_name}' deleted successfully.")
    return workspace

def main(): 
    # take the config.json file as an argument
    import sys
    if len(sys.argv) != 3:
        print("Usage: python admin_script.py <config.json>")
        exit(1)

    # Add another argument to accept either create or delete workspace
    operation = sys.argv[2]

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
        API_KEY = config["API_KEY"]
        WORKSPACE_NAME = config["WORKSPACE_NAME"]
        WORKSPACE_NAMESPACE = config["WORKSPACE_NAMESPACE"]
        CLUSTER_NAME = config["CLUSTER_NAME"]
        SECRET_NAME = config["SECRET_NAME"]
        USER_NAME = config["USER_NAME"]
        USER_EMAIL = config["USER_EMAIL"]
        PROJECT_NAMESPACE = config["PROJECT_NAMESPACE"]
        KUBECONFIG_FILE = config["KUBECONFIG_FILE"]

        # Placeholder for any further processing per team
        print(f"Completed processing for team: {team}\n{'='*50}")

        print("Starting GPU workload automation script...")

        # Admin Authentication with EGS    
        auth = authenticate(ENDPOINT,API_KEY)


        if operation == "create":
            # Admin Creates workspace
            workspace = create_workspace(auth, WORKSPACE_NAME, WORKSPACE_NAMESPACE, CLUSTER_NAME, USER_NAME, USER_EMAIL)
            
            print(f"Waiting for 10 seconds ...")
            time.sleep(10)
            # ask_to_continue("Get kubeconfig")
            kubeconfig = egs.get_workspace_kubeconfig(workspace_name=WORKSPACE_NAME, cluster_name=CLUSTER_NAME[0], authenticated_session=auth)
            print("Kubeconfig retrieved successfully.")
            
            # saving kubeconfig to a file
            subprocess.run(["mkdir", "-p", f"./{team}"], check=True)
            with open(f"./{team}/{WORKSPACE_NAME}-kubeconfig.yaml", "w") as f:
                f.write(kubeconfig)

            secret = subprocess.run(["kubectl", "--kubeconfig", KUBECONFIG_FILE, "get", "secrets", SECRET_NAME, "-n", PROJECT_NAMESPACE, "-o", "json"], capture_output=True, text=True, check=True)
            secret_json = json.loads(secret.stdout)
            token = secret_json['data']['token']
            token = base64.b64decode(token).decode('utf-8')
            
            # save the token to a file
            with open(f"./{team}/{WORKSPACE_NAME}-token.txt", "w") as f:
                f.write(token)

            # Create an empty file called api-token.txt under the team folder
            subprocess.run(["touch", f"./{team}/api-token.txt"], check=True)

        elif operation == "delete":
            Delete_workspace(auth, WORKSPACE_NAME)


if __name__ == "__main__":
    main()
