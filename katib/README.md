# Hyperparameter tuning using Katib:
Now, we will see a simple example as we did with the pipeline to make use of one of the best tools inside kubeflow i.e. Katib. We will try out a very simple example that will clear out the requirements for Katib. We can make use of the concept gained in the example to further develop hyperparameter tuning for any code.

We will first look into the python code required for katib training and also the docker file. 

Suppose if we have to maximize an objective metric total using 2 hyperparameters val1 and val2, where the objective metric total could take maximum value = 10.
We will look into it step by step:

**Python code:**
```
import argparse


def add(args):
    val1=args.val1
    val2=args.val2
    total=val1+val2
    print("total={}".format(total))
    

if __name__ == '__main__':

    # This python script will be our MAIN entrypoint, hence parsing here the command line arguments.
    parser = argparse.ArgumentParser(description="Training my_model()",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--val1', type=float, default=1,
                    help='value1')
    parser.add_argument('--val2', type=float, default=1,
                    help='value 2')


    args = parser.parse_args()
    add(args)
```

 Few things to take care in .py file for katib are:
1. Katib uses the argparse library to take arguments from the command line.
2. In order to specify a hyperparameter always use “--” before the hyperparameter.
3. The output should be <name_of_objective_metric>=<value> in this format only. Example: print("total={}".format(total))


**Create a dockerfile for the above python code.**
  
```  
FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y wget python3-dev gcc && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py

ADD . /add
WORKDIR /add


ENTRYPOINT ["python3", "/add/add.py"]
```

Now I am assuming that you have created a docker image, and both the python code and dockerfile is present in a docker container at a location **\<username>/<repo_name>**

The next step is to specify a katib job. There are 2 ways of doing this: i) Either by using UI itself, ii) or by having a YAML file.


**1. Using UI:** <br>

First, you need to specify the trial manifests inside katib: 

>Go to Kubeflow UI -> Katib -> Trial Manifests -> Add

In that you have to give the below-given yaml description, the things that you need to change are the docker image path **(docker.io/<your_user_name>/<repo_name>)** and how to execute the python file (this is similar to the last line of the docker file).

```
apiVersion: batch/v1
kind: Job
metadata:
  name: {{.Trial}}
  namespace: {{.NameSpace}}
spec:
  template:
    spec:
      containers:
      - name: {{.Trial}}
        image: docker.io/<your_user_name>/<repo_name>
        command:
        - "python3"
        - "add.py"
        - "--batch-size=64"
        {{- with .HyperParameters}}
        {{- range .}}
        - "{{.Name}}={{.Value}}"
        {{- end}}
        {{- end}}
      restartPolicy: Never
```
Then save it.

After this go to 
>HP -> submit -> Parameters

**Name:** It can be anything like random-experiment or add or the name of the model. <br>
**Namespace:** Generally keep this same as the kubeflow namespace. <br>
**Parameters:** Leave this as it is, it is used to specify how many parallel trials we want, total trials, and the number of failed trials we want. <br>
**Objective:** You can specify the objective parameters here like sometimes it can be rmse or loss or the accuracy, etc. In our case it is **total**. The **type is to maximize** the objective metric in our case and the **goal is 10**. There is also a field for an additional metric name which is not relevant for now, if you have then you can provide. <br>
**Algorithm:** You can select the type of algorithm like random, grid search, bayesian, etc. For now, select random. <br>
**Parameters:** You have to specify the parameter’s name and its type and also min and max value. In our case, it is **--val1 type=double min=1 and max=9** and **--val2 type=double min=1 and max=9**  <br>
**TrialSpec:** Inside this, there are two things. In namespace give kubeflow and in trialspec select the name of trial manifest that we created earlier.

And Deploy.

Now go to 
>HP -> Monitor -> (name of your experiment) <br>

And keep refreshing until you see a graph, sometimes it takes more time. <br>
If you see a graph, it means your code is running fine.


**2. You can also do all these things using a simple YAML file:** <br>
Go to 
>HP -> Submit. <br>

There in YAML file section give the below code(It will do the same thing that UI did):

```
apiVersion: "kubeflow.org/v1alpha3"
kind: Experiment
metadata:
  namespace: minikube
  labels:
    controller-tools.k8s.io: "1.0"
  name: add
spec:
  objective:
    type: maximize
    goal: 10
    objectiveMetricName: total
  algorithm:
    algorithmName: random
  parallelTrialCount: 3
  maxTrialCount: 12
  maxFailedTrialCount: 2
  parameters:
    - name: --val1
      parameterType: double
      feasibleSpace:
        min: "1"
        max: "9"
    - name: --val2
      parameterType: double
      feasibleSpace:
        min: "1"
        max: "9"
  trialTemplate:
    goTemplate:
      rawTemplate: |-
        apiVersion: batch/v1
        kind: Job
        metadata:
          name: {{.Trial}}
          namespace: {{.NameSpace}}
        spec:
          template:
            spec:
              containers:
              - name: {{.Trial}}
                image: docker.io/<your_user_name>/<repo_name>
                command:
                - "python3"
                - "add.py"
                {{- with .HyperParameters}}
                {{- range .}}
                - "{{.Name}}={{.Value}}"
                {{- end}}
                {{- end}}
              restartPolicy: Never
```

**I personally find YAML easier to use, the reasons behind it are:**
1. We can simply copy-paste our older yaml file and make changes accordingly.
2. We can try out new variations very quickly, but if we use UI then we have to fill all the details again.
3. We don’t have to specify trial manifest separately. We can do it inside our yaml file itself.

Congratulations!! You did your first hyperparameter tuning on kubeflow.
