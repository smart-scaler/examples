./istio-1.19.3/bin/istioctl install --skip-confirmation
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm install keda kedacore/keda --namespace keda --create-namespace
kubectl apply -f ./istio-1.19.3/samples/addons/prometheus.yaml
kubectl apply -f ./istio-1.19.3/samples/addons/grafana.yaml
helm install acme --set create_namespace=true --set stateful=true ./chart-acme
helm install boutique ./chart-boutique
