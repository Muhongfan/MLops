
from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule
from prefect.flow_runners import SubprocessFlowRunner


DeploymentSpec(
    flow_location="score.py",
    name="ride_duration_prediction",
    # https://docs.prefect.io/2.11.3/concepts/deployments/
    parameters={
        "taxi_type": "fhv",
        "run_id": "7c8bb75fadea44aa9337ec3de35c430e",
    },
    flow_storage="a68ce4f5-31cf-4484-87bb-8c2e7e70ad49",
    schedule=CronSchedule(cron="0 3 2 * *"),
    flow_runner=SubprocessFlowRunner(),
    tags=["ml"]
)