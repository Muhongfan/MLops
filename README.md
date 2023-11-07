Free MLOps course run by DataTalksClub. The program comprises seven modules followed by a capstone project as mentioned below and spans across several months.

Skills involve: AWS Kinesis, EC2, S3, LAMBDA, Prefect, Mlflow, PostgreSQL, Docker, Docker-compose, Grafana; Automation Test (Unit test/Integration test/Cloud service with localstack), Code quality check (pylint, black, isort,) 
 The ![Architecture](architecture.jpeg) MLops.

Module 1: Introduction
* [What is MLOps](https://www.youtube.com/watch?v=s0uaFZSzwfI&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK)
* Connect remote environment through Pycharm
* Edit remote jupyter notebook on the localhost
* Running example: training a ride duration prediction model
* Environment preparation (Anaconda, Docker, Docker Compose)
* Maturity models


Module 2: Experiment tracking and model management
* Why MLops
* Experiment tracking intro
* Experiment tracking with MLflow
* Model management 
* Model registry
* MLflow in practice
* MLflow: benefits, limitations and alternatives


Module 3: Orchestration and ML Pipelines
*Add workflow chart*
* Orchestration pipeline (Prefect)
* Turning a notebook into a pipeline
* Deployment of Prefect flow



Module 4: Model Deployment
*Add kinesis stream chart*
* Batch vs online
* For online: web services vs streaming
* Serving models in Batch mode
* Web services (Flask + MLflow + AWS s3)
* Streaming (PostgreSQL + AWS Lambda/Kinesis/s3)
* Batch

Module 5: Model Monitoring

* Intro to Model Monitoring, ML-based services, such as building batch monitoring, monitoring Scheme
* Monitoring batch jobs with Docker, Prefect, PostgreSQL, Evidently, and Grafana

<!--* Monitoring web services with Prometheus, Evidently, and Grafana-->


Module 6: Best Practices
* Testing: unit, integration
* Python: linting and formatting
* Pre-commit hooks and makefiles
* CI/CD (GitHub Actions)
* Infrastructure as code (Terraform)
* Automation Test (unit test, integration test with python, docker-compose; and cloud service test with LocalStack)
* code quality (pylint, git pre-commit, Makefile, AWS S3)



### Differences:
- Docker & Docker-compose
- Kafka & AWS Kinesis

