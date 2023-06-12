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
    
    ***Similar:*** [Cancel tracking](https://thedevpost.com/blog/remove-files-or-folders-from-remote-git/)

    ```
    # Remove a file
    git rm --cached readme1.txt // remove tracking but not phisically remove the file
    git rm --f readme1.txt  //remove the file
    ```
    ```
    # Remove a folder
    git rm --cached -rf .idea  // remove tracking (under current folder )but not phisically remove the file
    git rm --cached -rf **/.idea/   // remove the tracking (under each folder)
    git rm -rf .idea/    // remove tracking but not phisically remove the file
    ```

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
    
    ***ANS:*** `git ls-tree -r master --name-only`

5. Do not want to upload specific files(Cancel tracking)
   
    ***ANS:*** 

    1). Add all except the targets to commit `git add --all -- ':!path/to/file1`

    2). `touch .gitignore` to create `.gitignore`, then edit it as:
    ```
    target          //ignore target folder
    angular.json    //ignore angular.json
    log/*           //ignore all the files under /log
    css/*.css       //ignore all the .css files under /css
   ```
   and finally, `git add .`

6. `hint: Updates were rejected because the tip of your current branch is behind`. Since the remote is without any files.

    ***ANS:*** Force to push the files `git push -u origin main -f`
7. Delete commit
   
   ***ANS:*** Reset to staging. `git reset --soft HEAD^` 
    p.s. if check with `git status`, working area is no commits

8. See full history of log

    ***ANS:*** `git log --all --full-history` 

    ![log_his.png](images%2Flog_his.png)
9. Delete targets from specific folder

    ***ANS:*** `git rm --cached 02-experiment-tracking/ -r `
10. Show info of Commit History
    `git show 9ddc9dca00b --stat`

    ![git_show.png](images%2Fgit_show.png)

git push origin aff53c790ed13236fbfdfce5feee473324bc7a5a:master

11. `git merge` & `git rebase` 
    
[Git pull usage]https://www.atlassian.com/git/tutorials/syncing/git-pull
    
```
x--x--C1--C2--C3 (B)
    |
  (origin/B)

1). git merge -i C1~

x--x--C1--C2--C3 (B)
    |          ^
    |          |
  (origin/B) -->

2). git rebase -i C1~

 x--x--C2'--C1'--C3' (B)
    |
  (origin/B)
```
 
12. It is suitable for completely deleting large resources from git from a git project, including historical submission records. 
    If it's not enough to delete a file in a directory, as long as the file is in the commit record, there will be information about the file in `.git`. 
    Use `filter-branch` to forcibly modify the submission information, and erase the historical submission traces of a certain file, as if this file has never existed
    1). Root folder, run `git rev-list --all | xargs -rL1 git ls-tree -r --long | sort -uk3 | sort -rnk4 | head -10`
    2). Edit commit `git filter-branch --tree-filter "rm -f {filepath}" -- --all`
    3). Force to push it to remote `git push -f --all`

