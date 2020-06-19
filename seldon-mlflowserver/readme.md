# Deployment using Seldon Core:
Even though Kubeflow’s own serving tool called Kfserving is pretty good but it lacks proper documentation and exemplar setups. And moreover, it has a beta status for now so we decide to move on with Seldon core inside Kubeflow. 


Seldon core converts your ML models (Tensorflow, Pytorch, H2o, etc.) or language wrappers (Python, Java, etc.) into production REST/GRPC microservices.
Seldon handles scaling to thousands of production machine learning models and provides advanced machine learning capabilities out of the box including Advanced Metrics, Request Logging, Explainers, Outlier Detectors, A/B Tests, Canaries and more. <br>


## Seldon core in Kubeflow
Now, let’s see how we can setup Seldon core inside our Kubeflow environment. Seldon Core comes installed with Kubeflow, we just have to adjust a few things in order to get running. 

You need to ensure the namespace where your models will be served has:
1. An Istio gateway named kubeflow-gateway.
2. A label set as serving.kubeflow.org/inferenceservice=enabled.
 
Steps are as follows:
1. Create a new namespace:
>kubectl create ns seldon

2. Label the namespace so you can run inference tasks in it:
>kubectl label namespace seldon serving.kubeflow.org/inferenceservice=enabled

3. Create an Istio gateway in that namespace named kubeflow-gateway:

```
cat <<EOF | kubectl create -f -
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: kubeflow-gateway
  namespace: seldon
spec:
  selector:
    istio: ingressgateway
  servers:
  - hosts:
    - '*'
    port:
      name: http
      number: 80
      protocol: HTTP
EOF
```

4. Create an example SeldonDeployment with a dummy model:

```
kubectl apply -f - << END
apiVersion: machinelearning.seldon.io/v1alpha2
kind: SeldonDeployment
metadata:
  name: mlflow-deployment
  namespace: seldon
spec:
  name: mlflow-deployment
  predictors:
  - graph:
      children: []
      implementation: MLFLOW_SERVER
      modelUri: gs://seldon-mlflow/mlflow/elasticnet_wine
      name: wines-classifier
    name: mlflow-deployment-dag
    replicas: 1
END
```

5. Wait for the state to become available:
>kubectl get sdep mlflow-deployment -n seldon -o jsonpath='{.status.state}\n’

6. Port forward to the Istio gateway:
>kubectl port-forward $(kubectl get pods -l istio=ingressgateway -n istio-system -o jsonpath='{.items[0].metadata.name}') -n istio-system 8004:80

7. And in a new terminal, Send a prediction request:
>curl -s -d "{'data': {'ndarray': [[7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8]]}}"   -X POST http://localhost:8004/seldon/seldon/mlflow-deployment/api/v0.1/predictions    -H "Content-Type: application/json"

8. It should output something like this:
```
{
  "meta": {
    "puid": "kv97k8st6qu9dsr5gnuscm8gee",
    "tags": {
    },
    "routing": {
    },
    "requestPath": {
      "wines-classifier": "seldonio/mlflowserver_rest:0.2"
    },
    "metrics": []
  },
  "data": {
    "names": [],
    "ndarray": [5.079198907008106]
  }
}
 ```
