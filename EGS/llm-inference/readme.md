# 🚀 LLM Inference Deployment

This guide provides step-by-step instructions to **build**, **deploy**, and **test** a language model inference service using **Docker** and **Kubernetes**.

---

## 🛠️ Build Docker Image

1. **Build the Docker image** for your language model inference application:

   ```bash
   docker build -t <your-image-name>:<tag> .
   ```

2. **Push the image** to your container registry (e.g., Docker Hub, AWS ECR, etc.):
   ```bash
   docker push <your-image-name>:<tag>
   ```

---

## 🌐 Deploy on Kubernetes

1. **Apply the Kubernetes manifests** to deploy the service:

   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```

2. **Verify the service** is up and running:
   ```bash
   kubectl get svc my-llm-service
   ```

---

## 🔍 Get External IP

Retrieve the external IP of your Kubernetes service:

```bash
kubectl get svc my-llm-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

---

## ⚡ Test the Endpoint

1. Replace `<external-ip>` with the external IP obtained in the previous step.
2. Use `curl` to send a test request to the `/generate` endpoint:

   ```bash
   curl -X POST http://<external-ip>/generate    -H "Content-Type: application/json"    -d '{"input": "What is Kubernetes?"}'
   ```

3. 🎉 **Success!** You should receive a JSON response with the model-generated output.

---

## 📖 Example JSON Response

```json
[
  {
    "generated_text": "Kubernetes is an open-source platform designed to automate the deployment, scaling, and operation of application containers."
  }
]
```

---

## 📋 Requirements

Ensure you have the following installed and configured:

- 🐳 Docker
- ☸️ Kubernetes (minikube, GKE, EKS, etc.)
- 🛠️ Kubectl CLI
- 🌐 Internet access to pull Docker images and Hugging Face models
