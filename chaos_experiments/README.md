# Acme Fitness Cluster Deployment Guide

This guide provides step-by-step instructions to deploy the Acme Fitness application on your Kubernetes cluster, install Chaos Mesh for chaos engineering experiments, introduce HTTP chaos using a predefined configuration, and monitor metrics using Prometheus.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Install Acme Fitness on the Cluster](#install-acme-fitness-on-the-cluster)
3. [Sign up for smart-scaler account](#install--smart-scaler-agent)
4. [Install Chaos Mesh on the Cluster](#install-chaos-mesh-on-the-cluster)
5. [Introduce Chaos with HTTPChaos Configuration](#introduce-chaos-with-httpchaos-configuration)
6. [View Smart Scaler UI for metrics](#view-smart-scaler-ui-metrics)
7. [Additional Resources](#additional-resources)
8. [Troubleshooting](#troubleshooting)
9. [Contact](#contact)

---

## Prerequisites

Before proceeding, ensure you have the following tools installed and configured:

- **Kubernetes Cluster**: Access to a running Kubernetes cluster.
- **Helm 3**: Package manager for Kubernetes.
- **kubectl**: Kubernetes command-line tool.
- **Chaos Mesh CLI (Optional)**: For managing Chaos Mesh resources.


### Install Helm 3

If you don't have Helm installed, follow these steps:

# Download the latest Helm release
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

# Verify installation
helm version
# install--smart-scaler-agent

Sign up for an account at AWS Marketplace -  https://aws.amazon.com/marketplace/pp/prodview-rphu4g4tfs2te
Deploy the Smart Scaler agent on your cluster by following hte instructions at https://ui.saas1.smart-scaler.io/agents page


Install Acme Fitness on the Cluster

Deploy the Acme Fitness application using Helm with the following command:

```bash
helm install acme \
  --set create_namespace=true \
  --set stateful=false \
  ./chart-acme
```

# Install chaos mesh
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm repo update


# Check container runtime
run "kubectl get nodes -o wide" in the CONTAINER-RUNTIME column

# Select the appropriate command to install chaos-mesh depending on the container-runtime

# Default to /var/run/docker.sock
helm install chaos-mesh chaos-mesh/chaos-mesh -n=chaos-mesh --version 2.7.0

# /run/containerd/containerd.sock
helm install chaos-mesh chaos-mesh/chaos-mesh -n=chaos-mesh --set chaosDaemon.runtime=containerd --set chaosDaemon.socketPath=/run/containerd/containerd.sock --version 2.7.0

# introduce-chaos-with-httpchaos-configuration
kubectl apply experiments/503.yaml

# Alternative : Introduce chaos through the chaos-mesh ui
