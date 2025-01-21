# Acme Fitness Cluster Deployment Guide

This guide provides step-by-step instructions to deploy the Acme Fitness application on your Kubernetes cluster, install Chaos Mesh for chaos engineering experiments, introduce HTTP chaos using a predefined configuration, and monitor metrics using Prometheus.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Sign up for smart-scaler account](#install--smart-scaler-agent)
3. [Install Acme Fitness on the Cluster](#install-acme-fitness-on-the-cluster)
4. [Install Chaos Mesh on the Cluster](#install-chaos-mesh-on-the-cluster)
5. [Introduce Chaos with HTTPChaos Configuration](#introduce-chaos-with-httpchaos-configuration)
6. [View Smart Scaler UI for metrics](#view-smart-scaler-ui-metrics)


---

## Prerequisites

Before proceeding, ensure you have the following tools installed and configured:

- **Kubernetes Cluster**: Access to a running Kubernetes cluster.
- **Helm 3**: Package manager for Kubernetes.
- **kubectl**: Kubernetes command-line tool.
- **Chaos Mesh CLI (Optional)**: For managing Chaos Mesh resources.


### Install Helm 3

If you don't have Helm installed, follow these steps:

### Download the latest Helm release
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

### Verify installation
helm version

# install--smart-scaler-agent

Sign up for an account at AWS Marketplace -  https://aws.amazon.com/marketplace/pp/prodview-rphu4g4tfs2te
Deploy the Smart Scaler agent on your cluster by following hte instructions at https://ui.saas1.smart-scaler.io/agents page


# Install Acme Fitness on the Cluster

### Deploy the Acme Fitness application using Helm with the following command:

```bash
helm install acme \
  --set create_namespace=true \
  --set stateful=false \
  ./chart-acme
```

# Install chaos mesh on the Cluster
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm repo update

Follow instructions at https://chaos-mesh.org/docs/production-installation-using-helm/

# introduce-chaos-with-httpchaos-configuration
kubectl apply experiments/503.yaml

### Alternative : Introduce chaos through the chaos-mesh ui

# View Smart Scaler UI for metrics
### See metrics on https://ui.saas1.smart-scaler.io
