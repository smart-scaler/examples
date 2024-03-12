Install all services and create namespace :

`helm install <revision_name> --set create_namespace=true .`

Install individual services without creating namespace : 

`helm install <revision_name> --set provision={cart} .`

Install multiple services without creating namespace :

`helm install <revision_name> --set provision={cart,cart-redis} .`

Create multiple copies within same namespace without creating namespace :

`helm install <revision_name> --set copies=<number of copies> .`

Create statefulsets for databases instead of deployments without creating namespace :

`helm install <revision_name> --set stateful=true .`

All of the above options can be used in combination however the create_namespace=true can be true for only one of the many revisions