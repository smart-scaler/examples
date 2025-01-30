# EGS SDK Examples

In this directory, you will find sample code that uses the EGS SDK to demonstrate the following use cases:

## Admin Persona

### Day 0 - Setup Infra

- 🚀 Setup/Use Cluster with GPU resources
- 🛠️ Setup EGS Controller on an OKE Cluster
- 🔗 Register and onboard new cluster

### Day 1 - Monitoring and Observability

- 📊 Log into EGS UI for Best of Class Observability, Monitoring, and Management of GPU Resources

### Day 1 - Handle User/Team Requests for GPU Workspaces

- 🔐 Log in to UI
- 🔑 Create and Retrieve the admin API token
- 🛠️ Use the token to:
  - Provision WorkSpaces for the user
  - Set up the right RBAC to enable deployment
  - Return kubeconfig namespace (same as workspace name) and token/url to log into EGS

### Day 1 - Manage Production Inference/Agentic Workloads

- 🔐 Log in to UI
- ⚙️ Manage Production Inference/Agentic endpoints

## Developer/Engineer/Scientist Persona

### Day 0

- 📝 Request access to GPU Workspace from Admin. Will receive kubeconfig to the workspace, url/token to log into the EGS UI

### Day 1

- 🔐 Login to UI with token
- 🔑 Create and Retrieve the dev API token
- 🖥️ Use Kubectl to connect to the workspace
- 🚀 Deploy their GPU workload
- 🛠️ Use the dev API token to request GPR for the workspace:

  - Query the inventory to select the right node type
  - Assign the right priority
  - Assign the length of time for GPU to be available

- 📈 Monitor the health and status of the GPU requests and workloads

## Pre-Requisites

- 💻 Access to a Linux terminal connected to the internet
- 📦 kubectl

## How to Run the Code

1. Expose `EGS_ENDPOINT` and `EGP_API_KEY` as environment variables:

   - To get the `EGS_ENDPOINT`, run `kubectl get svc -n kubeslice-controller` and copy the `EXTERNAL-IP` of the `egs-core-apis` service and append `:8080` to it. Example: `http://<EXTERNAL-IP>:8080`
   - `EGP_API_KEY` can be obtained from the EGS UI

2. Place the admin kubeconfig file in the root directory of the project, and name it `admin-kubeconfig.yaml`

3. In the runner.py file, update the CLUSTER_NAME variable with the name of the cluster in your EGS account

4. Based on the requirement uncomment the code that calls admin_script or user_script in the runner.py file

5. Run `python3 runner.py` to generate sample workspaces and GPU requests
