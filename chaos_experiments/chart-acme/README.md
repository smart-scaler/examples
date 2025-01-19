# Acme Fitness Cluster Deployment Guide

This guide provides step-by-step instructions to deploy the Acme Fitness application on your Kubernetes cluster, install Chaos Mesh for chaos engineering experiments, introduce HTTP chaos using a predefined configuration, and monitor metrics using Prometheus.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Install Acme Fitness on the Cluster](#install-acme-fitness-on-the-cluster)
3. [Install Chaos Mesh on the Cluster](#install-chaos-mesh-on-the-cluster)
4. [Introduce Chaos with HTTPChaos Configuration](#introduce-chaos-with-httpchaos-configuration)
5. [View Prometheus Metrics](#view-prometheus-metrics)
6. [Additional Resources](#additional-resources)
7. [Troubleshooting](#troubleshooting)
8. [Contact](#contact)

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

Install Acme Fitness on the Cluster

Deploy the Acme Fitness application using Helm with the following command:

```bash
helm install acme \
  --set create_namespace=true \
  --set stateful=false \
  ./chart-acme
```

helm repo add chaos-mesh https://charts.chaos-mesh.org
helm repo update