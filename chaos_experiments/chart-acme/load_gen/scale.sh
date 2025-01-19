replicas=5

kubectl scale --replicas=$replicas deploy/cart-default-0                 
kubectl scale --replicas=$replicas deploy/cart-redis-default-0           
kubectl scale --replicas=$replicas deploy/catalog-default-0              
kubectl scale --replicas=$replicas deploy/catalog-mongo-default-0       
kubectl scale --replicas=$replicas deploy/order-default-0                
kubectl scale --replicas=$replicas deploy/order-postgres-default-0       
kubectl scale --replicas=$replicas deploy/payment-default-0              
kubectl scale --replicas=$replicas deploy/users-default-0                
kubectl scale --replicas=$replicas deploy/users-mongo-default-0          
kubectl scale --replicas=$replicas deploy/users-redis-default-0          