## Obtain the model and build the pipeline
### Step 1: organize [score.ipynb](score.ipynb)
### Step 2: transfer [score.ipynb](score.ipynb) to [score.py](score.py) with `jupyter nbconvert --to script score.ipynb`
### Step 3: Run [score.py](score.py) with  `python score.py green 2021 4 YOUR_RUN_ID`
## Deploy on prefect




## Note:
1. HTTPError: HTTP Error 403: Forbidden when call apply_model() in score.ipynb

**Solution**: instead of input_file = f'https://s3.amazonaws.com/nyc-tlc/trip+data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'  use input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'