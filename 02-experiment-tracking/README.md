# 1. Why MLops
## 1.1 Difference of DataOps vs MLOps vs DevOps
![ops.png](images/ops.png)

***"MLOps delivers machine learning models faster"***

*A set of practices to design, build and manage reproducible, testable and sustainable ML-powered software. 
For Big Data/Machine Learning teams, MLOps incorporate most DataOps tasks and additional ML-specific tasks, such as model versioning, testing, validation and monitoring.*

1. Compliance
In the MLOps realm, industries such as finance and healthcare often require model explainability. 

🔧 Tools: PySyft decouples private data for model training, AirCloak for data anonymisation. Awesome AI Guidelines for a curation of principals, standards and regulations around AI.

2. Iterative Development

3. Reproducibility
Machine learning models are often retrained because of either data drift. In order to reproduce the results, MLOps need to version the model and DataOps need to version the data. When being asked by an auditor which data was used to train which model to produce this specific result, the data scientist needs to be able to answer that.

🔧 Tools: experiment tracking tools, such as KubeFlow, MLFlow or SageMaker all have functionalities that link metadata to the experiment run. Pachyderm and DVC for data versioning.

4. Testing
From ML perspective, model accuracy, security, bias/fairness, interpretability all need to be tested.

🔧 Tools: libraries such as Shap & Lime for interpretability, fiddler for explainability monitoring, great expectation for data testing.

5. Continuous Deployment
There are three components to the continuous deployment of machine learning models.

- The first component is the triggering event, i.e. is the trigger a manual trigger by a data scientist, a calendar schedule event and a threshold trigger?
- The second component is the actual retraining of the new model. What are the scripts, data and hyperparameters that resulted in the model? Their versions and how they are linked to one another.
- The last component is the actual deployment of the model, which must be orchestrated by the deployment pipeline with alerting in place.

🔧 Tools: most workflow management tools have this, such as AWS SageMaker, AzureML, DataRobot, etc. Open-source tools such as Seldon, Kubeflow KFServing.

6. Automation
Automation is the core-value of DevOps, and really there are a bunch of tools specialised in different aspects of automation. Here are some resources for machine learning projects:

Awesome Machine Learning https://github.com/josephmisiti/awesome-machine-learning

Awesome Production Machine Learning https://github.com/ethicalml/awesome-production-machine-learning

7. Monitoring
Software applications need to be monitored, so does machine learning model and the data pipeline. 
For DataOps, it’s important to monitor the new data’s distribution for any data and/or concept drift. On the MLOps side, in addition to model degradation, it is also paramount to monitor adversarial attacks if your model has a public API.

🔧 Tools: Most workflow management framework has some form of monitoring. Other popular tools include Prometheus for monitoring metrics, Orbit by Dessa for data & model monitoring.


***Reference:*** https://towardsdatascience.com/what-the-ops-are-you-talking-about-518b1b1a2694


# 2. Experiment tracking and model management

* [Slides](https://drive.google.com/file/d/1YtkAtOQS3wvY7yts_nosVlXrLQBq5q37/view?usp=sharing)

## 2.1 Experiment tracking intro
### MLflow

MLflow is an open source platform to manage the ML lifecycle, including experimentation, reproducibility, deployment, and a central model registry. 
MLflow currently offers four components:

- MLflow Tracking
Record and query experiments: code, data, config, and results

- MLflow Projects
Package data science code in a format to reproduce runs on any platform

- MLflow Models
Deploy machine learning models in diverse serving environments

- Model Registry
Store, annotate, discover, and manage models in a central repository

***Ref:***  https://www.mlflow.org/

## 2.2 Getting started with MLflow
***Note*** *Run in the local environment.*
### Prepare the environment ###
Run the following command to create a fresh new new conda virtual environment.  
```conda create -n exp-tracking-env python=3.9```
  
Next we activate the newly created environment.  
```conda activate exp-tracking-env```
  
Install the required packages listed in requirements.txt file.  
```pip install -r requirements.txt```
```pip install -r requirements.txt``

Launch mlflow ui as well. Run the following command to start mlflow ui (a gunicorn server) connected to the backend sqlite database.  
```mlflow ui --backend-store-uri sqlite:///mlflow.db```

To access mlflow ui open `https://127.0.0.1:5000` in your browser.

## 2.3 Experiment tracking with MLflow
Linear model:
[duration-prediction.ipynb](para_tracking_duration-prediction.ipynb)
![lr.png](images%2Flr.png)

Xgboost:
[xgboost.ipynb](xgboost.ipynb)
![xgboost.png](images%2Fxgboost.png)

Ensemble:
[ensemble.ipynb](ensemble.ipynb)
![ensemble.png](images%2Fensemble.png)

## 2.4 Model management
* Load model as an artifact:
`mlflow.log_artifact("mymodel", artifact_path = "models/")`

* Log model using the method `log_model`:
`mlflow.<framework>.log_model(model, artifact_path = "models/")`

Examples are in [xgboost.ipynb](xgboost.ipynb):

* Load model as an artifact:
`mlflow.log_artifact("models/preprocessor.b", artifact_path="preprocessor")`

* Log model using the method `log_model`:
`mlflow.xgboost.log_model(model, artifact_path="models_mlflow")`

## 2.5 Model registry
Model Registry concepts to manage life cycle of mlflow model:

* Model - An mlflow model logged with one of the flavours `mlflow.<model_flavour>.log_model()`
* Registered model - An mlflow model registered on Model Registry. It has a unique name, contains versions, transitional stages, model lineage and other associated metadata. 
* Model Version - Version of the registered model 
* Model Stage - Each distinct model version can be associated with one stage at a time. Stages supported are Staging, Production and Archived. 
* Annotations and descriptions - Add useful information such as descriptions, data used, methodology etc. to the registered model.

![model_registry.png](images%2Fmodel_registry.png)
As we already run different models and collect the version information. We want to tag the models in different stages(staging, production, archived).
Considering the information of models, such as *Duration*, *Size*, ..., we `Register Model` for each selection, and name the new Model group as 'nyc_taxi_regressor'.
And see the comparison of the selections in `Models` on the top.

![registry.png](images%2Fregistry.png)
![Versions.png](images%2FVersions.png)

Then tag the stages of each selection.
![Versions.png](images%2FVersions.png)

Code for checking the versions: [model-registry.ipynb](model-registry.ipynb)


## 2.6 MLflow in practice


## 2.7 MLflow: benefits, limitations and alternatives




