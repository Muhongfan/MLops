# 4.Deployment
1. Create the folder "web-service"
2. Copy the `lin_reg.bin` file from the previous project
3. Install `pipenv` if you did not do it before (optional)
    `sudo -H pip install -U pipenv`
4. Check the current scikit-learn version, since only matched version can pickle the file.
    `pip freeze | grep scikit-learn`
5. Install the required version of scikit-learn (optional), flask and the python version that matches it.
    ` pipenv install flask --python=3.10`
6. Activate the virtual environment
    `pipenv shell`
6. Run the `test.py` 