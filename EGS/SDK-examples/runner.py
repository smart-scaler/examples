import json
import subprocess
import os
import time
# List of teams
teams = ["team-beta", "team-gamma", "team-delta", "team-epsilon"]

# Base configuration template
base_config = {
    "ENDPOINT": os.getenv("EGS_ENDPOINT"),
    "API_KEY": os.getenv("EGS_API_KEY"),
    "PROJECT_NAMESPACE": "kubeslice-avesha",
    "KUBECONFIG_FILE": "admin-kubeconfig.yaml"
}

# Generate config for each team
configs = {}
for team in teams:
    configs[team] = {
        "WORKSPACE_NAME": team,
        "WORKSPACE_NAMESPACE": [team],
        # use this as an env variable
        "CLUSTER_NAME": [f"worker-1"],
        "SECRET_NAME": f"kubeslice-rbac-rw-slice-{team}",
        "USER_NAME": f"{team}-user",
        "USER_EMAIL": f"{team}-user@avesha.io",
    }
    # Merge with base config
    configs[team].update(base_config)

# Save to config.json
with open("config.json", "w") as file:
    json.dump(configs, file, indent=4)

print("Config file 'config.json' has been generated successfully.")

# # Uncomment the following lines to create the workspaces
# # Run admin_script.py with the generated config file
# subprocess.run(["python", "admin_script.py", "config.json", "create"], check=True)
# # sleep for 60 seconds
# print("Waiting for 120 seconds ...")
# time.sleep(120)

# # Uncomment the following line to delete the workspaces
# subprocess.run(["python", "admin_script.py", "config.json", "delete"], check=True)

subprocess.run(["python", "user_script.py", "config.json"], check=True)