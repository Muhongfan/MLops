Free MLOps course run by DataTalksClub. The program comprises seven modules followed by a capstone project as mentioned below and spans across several months.

Module 1: Introduction
* [What is MLOps](https://www.youtube.com/watch?v=s0uaFZSzwfI&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK)
* Environment preparation
* Connect remote through Pycharm
* Edit remote jupyter notebook on your localhost
* Running example: training a ride duration prediction model
* Maturity models

Module 2: Experiment tracking and model management
* Why MLops
* Experiment tracking intro
* Getting started with MLflow 
* Experiment tracking with MLflow
  * Basic info login into MLflow 
    Example: [basic_mlflow.ipynb](02-experiment-tracking%2Fbasic_mlflow.ipynb)
  * Complicated info login into MLflow : 
    * Adding hyperparameter tuning into notebook using hyperopt 
    * Exploring results
    * How to select best model
    Example: [xgboost.ipynb](02-experiment-tracking%2Fxgboost.ipynb) &
             [ensemble.ipynb](02-experiment-tracking%2Fensemble.ipynb)
* Model management 
  * Save model
    
    * `with open("models/preprocessor.b", "wb") as f_out:
          pickle.dump(dv, f_out)`

  * Load model(2 ways): 
    * Load model as an artifact:
      `mlflow.log_artifact("mymodel", artifact_path = "models/")`

    * Log model using the method `log_model`:
      `mlflow.<framework>.log_model(model, artifact_path = "models/")`

* Model registry
  * register models
  * transfering models different stages
  * How to select the best model based on the performance
  * How to test on the valid dataset
  
  Example: [model-registry.ipynb](02-experiment-tracking%2Fmodel-registry.ipynb)
* MLflow in practice
* MLflow: benefits, limitations and alternatives

