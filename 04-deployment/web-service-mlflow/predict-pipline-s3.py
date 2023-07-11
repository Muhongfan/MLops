import os

import pickle
import sklearn
from flask import Flask, request, jsonify
import mlflow
from mlflow.tracking import MlflowClient
# Start the instance without connecting to tracing server

# MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

RUN_ID = os.getenv('RUN_ID')

# RUN_ID = '7c8bb75fadea44aa9337ec3de35c430e'

logged_model = f's3://zoomcamp-mlops/1/{RUN_ID}/artifacts/model'
# Load model as a PyFuncModel.
# logged_model = f'runs:/{RUN_ID}/model'

model = mlflow.pyfunc.load_model(logged_model)





def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    preds = model.predict(features)
    return float(preds[0])


app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
# wrapper for the above funcs that will take requrests web requests http requests
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        'duration': pred,
        'model_version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)