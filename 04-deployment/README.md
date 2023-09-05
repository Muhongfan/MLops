## Deployment Types:
There are 2 types/paradigms or deployment:

1. Offline(Batch Deployment):

    Not real-time prediction. Periodical prediction in hourly, daily, monthly time slot. 
    We have a database, and a scoring job (model).
    The scoring job periodically pulls data from the database any time it reuires and runs the model on it. 
    The result is written on a predictions DB.

    Example: Churn job.
    ![offline.png](images%2Foffline.png)
2. Online:

    The model is always available for prediction. There are two ways to deploy an online model:

  - Web Service:
    Periodical real-time forecasting(hourly, daily, monthly) depends on the interval set.

    The relationship(nums) between the client (the Backend in this case) and the model is 1 to 1.

    Example: Our Taxi duration prediction. 

    ![webservice.png](images%2Fwebservice.png)
  - Streaming:
    
    **Note**: stream can be regarded as a agent, so both producers (who produce data) and consumers (who predict) do not have direct connection but communicating via stream.

    We have a producer(s) and consumers. The producer pushes some data into a data stream and the consumers cna get the data for their tasks. 

    The relationship(nums) between the client (the Backend in this case) and the model is 1 to N.

    Example: The backend (producer) pushes the data into the data stream alongside an event Ride_started; Consumer 1 (C1) predicts the duration, C2 predicts the cost, C3 predicts the Tip...etc

    ![streaming.png](images%2Fstreaming.png)

    The consumers could also push their predictions to a prediction stream and a decision service will act on their predictions and considered by producers.
  
    Example: A Youtuber update his/her content to the platform, the data can be sent to the stream, and the consumers (different models) can make a prediction based on the data obtained. The predictions are all sent to prediction stream and final decision could be sent to producer (User).

    ![mul-stream.png](images%2Fmul-stream.png)

## Notes:
1. Offline: [Batch](https://github.com/Muhongfan/MLops/blob/main/04-deployment/Batch/REAMME.md)
2. Online:
   - Web service: 
     * [Web service](https://github.com/Muhongfan/MLops/blob/main/04-deployment/web-service/README.md)
     * [web-service-mlflow](https://github.com/Muhongfan/MLops/blob/main/04-deployment/web-service-mlflow/README.md)
   - Streaming:
     * [Streaming](https://github.com/Muhongfan/MLops/blob/main/04-deployment/streaming/README.md)
