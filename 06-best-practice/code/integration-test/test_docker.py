# pylint: disable=duplicate-code
import sys
import json
import logging

from deepdiff import DeepDiff

import lambda_function

logging.getLogger("mlflow").setLevel(logging.DEBUG)

sys.path.append("..")


with open('event.json', 'rt', encoding='utf-8') as f_in:
    event = json.load(f_in)


url = 'http://localhost:8080/2015-03-31/functions/function/invocations'
# response = requests.post(url, json=event)
# print("Hello Piggy")
# print(response.text)
# print("Hello Puppy")
actual_response = lambda_function.lambda_handler(event, None)
print('acutual response')

print(json.dumps(actual_response, indent=2))

expected_response = {
    'predictions': [
        {
            'model': 'ride_duration_prediction_model',
            'version': '7c8bb75fadea44aa9337ec3de35c430e',
            'prediction': {
                'ride_duration': 18.2,
                'ride_id': 156,
            },
        }
    ]
}
diff = DeepDiff(actual_response, expected_response, significant_digits=1)
print(f'diff={diff}')
assert 'type_changes' not in diff
assert 'values_changed' not in diff
# diff={}
# assert actual_response == expected_response
