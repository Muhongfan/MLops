# 4.Deployment

1. Create the folder "web-service"
2. Copy the `lin_reg.bin` file from the previous project

3. Install `pipenv` if you did not do it before (optional)
    
    `sudo -H pip install -U pipenv`
4. Check the current scikit-learn version, since only matched version can pickle the file.
    
    `pip freeze | grep scikit-learn`
   - `freeze`: show all the libraries that we currently have installed
5. Install the required version of scikit-learn (optional), flask and the python version that matches it.
    
    `pipenv install scikit-learn==1.2.2 flask --python=3.10`
   -> generate `pipfile` and `pipfile.lock
7. Activate the virtual environment
    
    `pipenv shell`
6. Creating a script without Flask for prediction and test files. Run the `test.py` 
   
    `python test.py`
7. Creating a script with Flask for prediction and test files. Run the `test.py` 

   `python test.py`
8. Since `WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.`, install gunicorn

   `gunicorn --bind=0.0.0.0:9696 predict:app`
9. Creating a script in `gunicorn` for prediction and test files. Run the `test.py` 

   `python test.py`
10. Lauch subshell in virtual environment

   `pipenv shell`
11. Install  `dev` dependency 

    `pipenv install --dev requests`
12. Write down a Dockerfile.
13. Build docker image.
   `docker build -t ride-duration-prediction-service:v1 .`

15. Run docker image

   `docker run -it --rm -p 9696:9696  ride-duration-prediction-service:v1`


## Note:
`docker build -t ride-duration-prediction-service:v1 .`

`docker run -it --rm -p 9696:9696  ride-duration-prediction-service:v1`

- `run`: create the container
- `-it`: interact via terminal
- `--rm`: remove the container if there is a crush
- `-p`: port to get access the container

