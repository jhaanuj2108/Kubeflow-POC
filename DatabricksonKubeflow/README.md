# Databricks Connection and MLFlow:
Now for databricks connection and in order to track MLFlow on databricks, we need to configure databricks. So, for that, we need to have Kale + Rok image in the notebook server. I have created my own kale + rok image which can be accessed by providing the custom image in the notebook server as jhaanuj2108/kale-rok.


----------------------------------------------------------------------------------------------------------------------------------------
```
FROM gcr.io/arrikto-public/tensorflow-1.14.0-notebook-cpu:kubecon-workshop
 
USER root
 
RUN pip install pandas
RUN pip install seaborn
RUN pip install scikit-learn
RUN pip install --upgrade pip
 
 
RUN pip install jupyterlab
RUN pip install https://storage.googleapis.com/ml-pipeline/release/latest/kfp.tar.gz --upgrade
 

RUN pip install kubeflow-kale
 

RUN jupyter labextension install kubeflow-kale-launcher
ENV NB_PREFIX /
CMD ["sh", "-c", \
     "jupyter lab --notebook-dir=/home/jovyan --ip=0.0.0.0 --no-browser \
      --allow-root --port=8888 --LabApp.token='' --LabApp.password='' \
      --LabApp.allow_origin='*' --LabApp.base_url=${NB_PREFIX}"]
```
----------------------------------------------------------------------------------------------------------------------------------------


The reason for having kale + rok image even though when it is creating some issues related to PVC is that kale + rok uses arrikto’s base image whereas having only kale uses tensorflow’s base image. So what that means is, in a notebook server’s terminal which was created using kale image we don’t see the root access.


Whereas the notebook server which was created using kale+rok image has the root access.


So, this is the main reason that we can configure databricks in our kale-rok notebook server and not in the kale notebook server.

In order to configure databricks and setup mlflow through kubeflow, we have to do a few things.

Install MLflow in the terminal using 
```
pip install mlflow
```

**Note: You might face this error** 

> AttributeError: module 'enum' has no attribute 'IntFlag'
In that case, first, do 
```
pip uninstall -y enum34 
```
and then do 
```
pip install mlflow.
```

After this, we have to (generate a rest API token)[https://docs.databricks.com/dev-tools/api/latest/authentication.html#token-management] to configure databricks.
**NOTE: Write down or save the token somewhere, because if lost you will not be able to find the same token. You will have to create a new token.**

Then run this command: 
```
 databricks configure --token
 ```
You will be prompted to:
```
Databricks Host (should begin with https://): <Your_databricks_host_like https://companyname.cloud.databricks.com/>

Token: <Insert the generated token>
```

Also, save the credentials as environment variables.
```
export MLFLOW_TRACKING_URI=databricks
export DATABRICKS_HOST="..."
export DATABRICKS_TOKEN="..."
```
You will also need to configure dbfs.
Do this: 
```
dbfs configure --token
Databricks Host (should begin with https://):<Your_databricks_host>
Token: <Insert the generated token>
```
