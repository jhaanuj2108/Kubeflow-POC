# Creating a notebook server:

After you have installed your kubeflow now it’s time to make use of every aspect of it. First thing first, let’s create a new notebook server:

On the left panel of kubeflow dashboard go to Notebook Server and then you can see create new server:

 
**Name:** You can specify any name to your notebook server, for example, “my-first-notebook” <br>

**Image:** Image is one of the most important things to take care of while creating a notebook. This asks for a docker image, there are 4 predefined images provided by Tensorflow which has variations to choose from either TF1.14 or TF2.1 and CPU/GPU. Here you can also give your **custom image (<docker_username>/<repo_name>)**. <br>

**Workspace Volume:** It is the main volume that the notebook server will be using, you can either create a new volume or use existing volume which you created for some other notebook server so that you can use the shared memory functionality.<br>

**Data Volume:** It is used to store some specific data like CSV files or any outputs, etc.<br>

**We can leave configuration and GPU as it is (Edit GPU only when you are using it).**<br>

**And now you can launch your notebook server.**<br>

>Go To Kubeflow UI -> Notebook Servers

There you can see the name of the new notebook server that you created

Now you can connect to notebook server using connect, <br>
>**Note:** Sometimes you may find an error saying “No healthy upstream found” but that is normal, wait a few more seconds and it will be fine. If the problem still persists for more than a minute then there might be one of the two problems: i) Either the way you have provided the custom image in the notebook server is wrong, or ii) Your docker image has some issue.
 
Once you connect successfully, you will find a Jupyter notebook where you can run your ipynb code. 
Note: There might be an issue in importing packages so you have to install the package by either of two ways:
1. In your jupyter notebook, you can give the command as pip install pandas
2. Or you can create a new terminal using jupyter notebook home and there you can use: pip install pandas.

Now, this is all about the Jupyter notebook and Notebook server in general.
