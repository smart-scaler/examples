helm uninstall acme
helm uninstall boutique
#helm uninstall keda
kubectl delete -f ./istio-1.19.3/samples/addons/grafana.yaml
kubectl delete -f ./istio-1.19.3/samples/addons/prometheus.yaml
#./istio-1.19.3/bin/istioctl uninstall --skip-confirmation --revision default
