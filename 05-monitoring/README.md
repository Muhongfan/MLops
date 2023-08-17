## Intro

### Why we need to monitor models after deployment?

| Production | Key Questions|
|--------|-----|
| Data distribution changes | Why are there sudden changes in the values of my features?|
|Model ownership in production | Who owns the model in production? The DevOps team? Engineers? Data Scientists?|
|Training-serving skew|Why is the model giving poor results in production despite our rigorous testing and validation attempts during development?|
|Model/concept drift|Why was my model performing well in production and suddenly the performance dipped over time?|
|Black box models|How can I interpret and explain my model’s predictions in line with the business objective and to relevant stakeholders?|
|Concerted adversaries|How can I ensure the security of my model? Is my model being attacked?|
|Model readiness|How will I compare results from a newer version(s) of my model against the in-production version(s)?|
|Pipeline health issues|Why does my training pipeline fail when executed? Why does a retraining job take so long to run?|
|Underperforming system|Why is the latency of my predictive service very high? Why am I getting vastly varying latencies for my different models?|
|Cases of extreme events (outliers)|How will I be able to track the effect and performance of my model in extreme and unplanned situations?|
|Data quality issues|How can I ensure the production data is being processed in the same way as the training data was?|

So we have to:
- monitor model performance in production: see how accurate the predictions of your model are. See if the model performance decays over time, and you should re-train it.
- monitor model input/output distribution: see if the distribution of input data and features that go into the model changed? Has the predicted class distribution changed over time? Those things could be connected to the data and concept drift.
- monitor model training and re-training: see learning curves, trained model predictions distribution, or confusion matrix during training and re-training.
- monitor model evaluation and testing: log metrics, charts, prediction, and other metadata for your automated evaluation or testing pipelines
- monitor hardware metrics: see how much CPU/GPU or Memory your models use during training and inference.
- monitor CI/CD pipelines for ML: see the evaluations from your CI/CD pipeline jobs and compare them visually. In ML, the metrics often only tell you so much, and someone needs to actually see the results.

Ref: 
* [A Comprehensive Guide on How to Monitor Your Models in Production](https://neptune.ai/blog/how-to-monitor-your-models-in-production-guide)
* [Best Tools to Do ML Model Monitoring](https://neptune.ai/blog/ml-model-monitoring-best-tools)
### What is data drift

Data drift, or covariate shift, refers to the phenomenon where the distribution of data inputs that an ML model was trained on differs from the distribution of the data inputs that the model is applied to. This can result in the model becoming less accurate or effective at making predictions or decisions.

Ref: 
[Data Drift vs. Concept Drift: What Is the Difference?](https://www.dataversity.net/data-drift-vs-concept-drift-what-is-the-difference/#:~:text=Data%20drift%20refers%20to%20the,of%20a%20machine%20learning%20model.)
### How is machine learning monitoring different?
Main:
- Service Health
Monitored by few metrics, which is also a must since have to make sure the service works.
- Model Health
Check how good the service provided. Evaluation metrics are based on tasks, for example, searching/recommendation system requires ranking metrics; regression requires
MAE or MAP; classification requires Log loss, precision or recall.
- Data quality and integrity
Check catch for the data quality when receiving and generating outputs, metrics such as share or missing values or count time, value range for each kind.
- Data and concept drift
Check the distribution of input and output which may be effected by real-world environment 

Others:
- Performance by segments
Check the quality metrics by segments when diverse objects/categories
- Bias and fairness
- Outliers
- Explainability

### Monitoring types
Batch Monitoring:

Online (non-batch) Monitoring:

### What is monitoring scheme
- Use Service: Implement the service as REST API or batch pipeline.
- Obtain logs: Generate logs as local log file when using the service
- Calculate Metrics based on logs
- Load Metrics into a Database: save the calculated metrics into a PostgreSQL database.
- Build a Dashboard: Use Grafana to build a dashboard with the data from PostgreSQL database.

## Build Monitoring Scheme
### Environment set up
**Step 1**: Build virtual environment
```
mkdir taxi_monitoring
cd taxi_monitoring
conda create -n py11 python=3.11
conda activate py11
```

**Step 2**: Install a requirement.txt
`pip install -r requirement.txt`

**Step 3**: Build Docker compose
1. install Docker compose with `conda install docker-compose`
2. Write a [docker-compose.yml](taxi_monitoring%2Fdocker-compose.yml) and [grafana_datasources.yaml](taxi_monitoring%2Fconfig%2Fgrafana_datasources.yaml) (Under ./config) install it with 
`docker-compose up --build`
![docker-compose.png](img%2Fdocker-compose.png)
3. Go to Grafana by `localhost:3000`. with 
```
username: `admin` 
pwd: `admin`, 
```
then change to your own pwd.
4. Go to adminer by `localhost:8080`, with 
```
System: PostgreSQL
Server: db
Username: postgres
Password: example	
Database: test
```


### Prepare reference and model
Make the dirs for the project and prepare
```
conda activate py11
docker-compose down
mkdir data
mkdir models
```
Then write the code as [baseline_model_nyc_taxi_data.ipynb](taxi_monitoring%2Fbaseline_model_nyc_taxi_data.ipynb)


### Evidently metrics calculation
See details in [baseline_model_nyc_taxi_data.ipynb](taxi_monitoring%2Fbaseline_model_nyc_taxi_data.ipynb) about data drift between reference data (training data) and current data (val data) and other metrics.


### Dummy monitoring

**Step 1**: Code for dummy metrics calculation as [dummy_metrics_calculation.py](dummy_metrics_calculation.py)

**Step 2**: Build services by docker-compose with `docker-compose up --build` 

**Step 3**: Check SQL on browser with `localhost:8080`.

**Step 4**: Build services on System: `PostgreSQL`, login info is in [grafana_datasources.yaml](taxi_monitoring%2Fconfig%2Fgrafana_datasources.yaml).
Here is what can be seen from sql.

![sql.png](img%2Fsql.png)

**Step 5**: Create a new dashboard and see the results as follows

![grafana.png](img%2Fgrafana.png)


### Data quality monitoring
**Step 1**: Compared with [dummy_metrics_calculation.py](taxi_monitoring%2Fdummy_metrics_calculation.py), we loaded the reference data, models and the needed compared data, also report for metrics calculation; we also changed `calculate_metrics_postgresql` for insert necessary metrics into postgresql; all changes can be seen in [evidently_report_example.py](taxi_monitoring%2Fevidently_report_example.py).
Run `python evidently_metrics_calculation.py` and login `localhost:8080` to see if it works.
![data_quality_sql.png](img%2Fdata_quality_sql.png)

**Step 2**: Build Prefect pipeline (Add @task/@flow)

**Step 3**: Start Prefect server and run the script with `prefect server start` and `python evidently_metrics_calculation.py` in different terminals. The results should be:

![prefect.png](img%2Fprefect.png)

**Step 4**: Access Grafana with `localhost:3000` and create the new dashboard.

![dashboard.png](img%2Fdashboard.png)


### Save Grafana Dashboard

**Step 1**: Create a [grafana_dashboards.yaml](taxi_monitoring%2Fconfig%2Fgrafana_dashboards.yaml) file under `./config`

**Step 2**: Add the following content to docker-compose file for updating dashboards info.
```
      - ./config/grafana_dashboards.yaml:/etc/grafana/provisioning/dashboards/dashboards.yaml:ro
      - ./dashboards:/opt/grafana/dashboards
```
**Step 3**: Create new `dashboards` dict and create a `data_drift.json` for Grafana. Copy the json data from the dashboards generated in the last step.

**Step 4**: Restart docker-compose with ```docker-compose down docker-compose up```, and go to Grafana to check the dashboards we saved.

![new_dashboards.png](img%2Fnew_dashboards.png)

![dashboard.png](img%2Fdashboard.png)

### Debugging with test suites and reports

[debugging_nyc_taxi_data.ipynb](taxi_monitoring%2Fdebugging_nyc_taxi_data.ipynb)
### Note: 
1. `grafana_1 | Error: ✗ Datasource provisioning error: read /etc/grafana/provisioning/datasources/datasource.yaml: is a directory`

**Solutions**: `docker-compose rm` then restart it with `docker-compose up --build`

2. `OSError: [Errno 30] Read-only file system: './data'` since can not find the relative path 

**Solutions**:
- Change path './data' to absolute address
- Or change the config file of jupyter notebook 
    ```
    jupyter notebook --generate-config 
    cd /Users/amberm (YOUR_USER_NAME)/.jupyter
    vim jupyter_notebook_config.py
    ```
   and then change the default path to the one under your path
   ```
   ## The directory to use for notebooks and kernels
   #  Default: ''
   c.NotebookApp.notebook_dir = 'YOUR_PRO_PATH'
  ``` 
  
3. Install evidently package

**Solutions**:
`conda install -c conda-forge evidently`
