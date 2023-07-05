import pickle

with open('/Users/amberm/PycharmProjects/MLops/04-deployment/web-service/lin_reg.bin', 'rb') as f_in:

    (dv, model) = pickle.load(f_in)

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return float(preds[0])