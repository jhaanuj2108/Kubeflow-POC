# Development in a full circle starting with a notebook to deployment including pipelines and Hyperparameter tuning:

**NOTE: It is suggested that you first look and understand every other folder of this Github repo then come back here.**

This is one of the most important phase of the POC. Earlier what we did was set up everything and try out some simple examples. Now, we will try to implement everything starting from a python notebook for a wine data then creating the required file for hyperparameter tuning using Katib and then creating a pipeline for that notebook and finally deploying the best model using the hyperparameters gained after training.

You can download the whole folder from the Github repo Kubeflow POC > End-to-end.

## Creating an ipynb notebook file:
I have created an ipynb notebook file for the wine dataset named as 1.train.ipynb. You can run that file which is based on MLFlow but note that here we are reducing the dependency with databricks so all the model logging and saving parameters are done in our local file inside the notebook server.
There are various runs/trials and the results and artifacts are stored in our local notebook server in a folder named “mlruns”.

## Hyperparameter tuning: 
For this step as mentioned earlier, we need to have two major files. One is the .py file which makes use of the argparse library and the other is the dockerfile.

In the folder, you will have 2.katib.py file and Dockerfile, create a docker image for those two files. You can also use a docker image created by me for the same two files: jhaanuj2108/katib-mlflow.
You can follow the steps for hyperparameter tuning that is given in katib folder in this Github repo itself.

## Creating a pipeline:
Now creating pipelines is an important part of the ML workflow. So, we can either run pipeline after hyperparameter tuning or before it, it basically depends on our usage. I have created a 4.pipeline.ipynb file which has all the annotations required for Kale to create a pipeline. I have used the best hyperparameters value in this case but the main motive is to include it in the workflow.

## Deploying the model:
We made use of Seldon Core to deploy the model. After tuning the hyperparameter, I made use of the best parameters and trained the model one last time and saved the model by using MLFlow in a folder call "best run".
You will get 3 files if you go into the "bestmodel", and the three files are: 
MLmodel, model.pkl, conda.yaml. Now, you have to create a public cloud bucket either using GCP storage or AWS S3. For this purpose, I made use of GCP storage. Make sure that these three files are available inside the bucket and the bucket is publicly available, and below in the next command where model_uri is asked give the URI of your bucket.

After this, you just have to run a kubectl command from your aws machine.

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

This will deploy a mlflow-deployment model. Wait till your model is available. To check its availability give this command:

>kubectl get sdep mlflow-deployment -n seldon -o jsonpath='{.status.state}\n'

It will show as creating for a few minutes then it will show available. Even for a long time (maybe 15-30 mins) it is still showing creating then there is something wrong with the files inside the bucket or maybe the bucket itself.

Once it shows as available. Now you can send a REST API request for prediction. In the same AWS EC2’s terminal give this command:

>kubectl port-forward $(kubectl get pods -l istio=ingressgateway -n istio-system -o jsonpath='{.items[0].metadata.name}') -n istio-system 8004:80


It will port forward the istio gateway on port 8004. 


And after this keep this terminal running, and open a new terminal. There you can give the command:

>curl -s -d "{'data': {'ndarray': [[7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8]]}}"   -X POST http://localhost:8004/seldon/<Your-seldon-namespace>/<Your-deployment-name>/api/v0.1/predictions    -H "Content-Type: application/json"

Example of localhost: http://localhost:8004/seldon/seldon/mlflow-deployment/api/v0.1/predictions
