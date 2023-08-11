#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import uuid
import pickle
import sys
from datetime import datetime
import pandas as pd

import mlflow
from prefect import task, flow, get_run_logger
from prefect.context import get_run_context

from dateutil.relativedelta import relativedelta


from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline


# In[2]:


# get_ipython().system('mkdir output/green')


# In[3]:


# year = 2021
# month = 2
# taxi_type = 'green'
#
# input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
# output_file = f'output/{taxi_type}/{year:04d}-{month:02d}.parquet'
#
# RUN_ID = os.getenv('RUN_ID', '7c8bb75fadea44aa9337ec3de35c430e')


# In[4]:


def generate_uuids(n):
    ride_ids = []
    for i in range(n):
        ride_ids.append(str(uuid.uuid4()))
    return ride_ids

def read_dataframe(filename: str):
    df = pd.read_parquet(filename)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    
    df['ride_id'] = generate_uuids(len(df))

    return df


def prepare_dictionaries(df: pd.DataFrame):
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']

    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts


# In[5]:
def save_results(df, y_pred, run_id, output_file):
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['lpep_pickup_datetime'] = df['lpep_pickup_datetime']
    df_result['PULocationID'] = df['PULocationID']
    df_result['DOLocationID'] = df['DOLocationID']
    df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred
    df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']
    df_result['model_version'] = run_id

    df_result.to_parquet(output_file, index=False)


def load_model(run_id):
    logged_model = f's3://zoomcamp-mlops/1/{run_id}/artifacts/model'
    model = mlflow.pyfunc.load_model(logged_model)
    return model


@task
def apply_model(input_file, run_id, output_file):
    logger = get_run_logger()

    logger.info(f'reading the data from {input_file}...')
    df = read_dataframe(input_file)
    dicts = prepare_dictionaries(df)

    logger.info(f'loading the model with RUN_ID={run_id}...')
    model = load_model(run_id)

    logger.info(f'applying the model...')
    y_pred = model.predict(dicts)

    logger.info(f'saving the result to {output_file}...')

    save_results(df, y_pred, run_id, output_file)
    return output_file


# In[6]:


# apply_model(input_file=input_file, run_id=RUN_ID, output_file=output_file)

def get_paths(run_date, taxi_type, run_id):
    prev_month = run_date - relativedelta(months=1)
    year = prev_month.year
    month = prev_month.month

    input_file = f's3://nyc-tlc/trip data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f's3://zoomcamp-mlops/taxi_type={taxi_type}/year={year:04d}/month={month:02d}/{run_id}.parquet'

    return input_file, output_file

@flow
def ride_duration_prediction(
        taxi_type: str,
        run_id: str,
        run_date: datetime = None):
    if run_date is None:
        ctx = get_run_context()
        run_date = ctx.flow_run.expected_start_time

    input_file, output_file = get_paths(run_date, taxi_type, run_id)

    apply_model(
        input_file=input_file,
        run_id=run_id,
        output_file=output_file
    )


def run():
    taxi_type = sys.argv[1]  # green
    year = int(sys.argv[2])  # year
    month = int(sys.argv[3])  # month
    run_id = sys.argv[4]  # 7c8bb75fadea44aa9337ec3de35c430e

    # output_file = f's3://duration-prediction/taxi_type={taxi_type}/year={year:04d}/month={month:02d}/{RUN_ID}.parquet'


    #
    # input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    # output_file = f's3://zoomcamp-mlops/output/{taxi_type}/{year:04d}-{month:02d}.parquet'

    # RUN_ID = os.getenv('RUN_ID', '7c8bb75fadea44aa9337ec3de35c430e')

    ride_duration_prediction(
        taxi_type=taxi_type,
        run_id=run_id,
        run_date=datetime(year=year, month=month, day=1)
    )


# get_ipython().system('ls output/green/')


if __name__ == '__main__':
    run()
