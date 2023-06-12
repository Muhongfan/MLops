# Problems 

### MLFLOW
1. **Can't connect to ('127.0.0.1', 5000) Running the mlflow server failed. Please see the logs above for details.**

    ***ANS:*** `ps aux | grep gunicorn` and then manually `kill [PID]`

2. **mlflow.exceptions.MlflowException: Could not find experiment with ID 0**

    ***ANS:*** Pay attention to the current location you run MLflow, should be the location with the experiments.

3. **MlflowException: Cannot set a deleted experiment 'nyc-taxi-experiment' as the active experiment. You can restore the experiment, or permanently delete the experiment to create a new one.**

  ***ANS:*** `mlflow gc --backend-store-uri sqlite:///mlflow.db(replace with your PATH)`
4. `[2023-06-09 16:54:01 -0400] [21091] [ERROR] Connection in use: ('127.0.0.1', 5000)
  [2023-06-09 16:54:01 -0400] [21091] [ERROR] Retrying in 1 second.`

    ***ANS:*** `kill -9 $(lsof -i:5000 -t) 2> /dev/null` kill the task that is using port 5000

### Git
1. `(modified content, untracked content)`
    
    ***ANS:*** Jump to the target folder,  `rm -rf .git*`
2. After ` git push origin main`, message as `git@github.com: Permission denied (publickey). 
  fatal: Could not read from remote repository.
     Please make sure you have the correct access rights
     and the repository exists.`

    ***ANS:*** 
    1. Generate Public Key
    ```
    ssh-keygen -t rsa -C YOUREMAIL
    ssh -v git@github.com
    ssh-add ~/.ssh/id_rsa
    ```
    2. Then, `vim id_rsa.pub ` to copy the key info, and go to your account in Github 'Setting' -> 'SSH and GPG keys' -> 'new SSH key', paste the key info.
    
    3. Finally, `ssh -T git@github.com ` and shows message as "Hi XXX! You've successfully authenticated, but GitHub does not provide shell access."

3.  ` git pull origin main` But shows message `fatal: refusing to merge unrelated histories`
    
    ***ANS:*** ` git pull origin main --allow-unrelated-histories`

4. Tracking files
    `git ls-tree -r master --name-only`

5. Do not want to update specific files
   `git add --all -- ':!path/to/file1`

6. 