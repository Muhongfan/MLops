
## 01-intro
1. Github - Token for identification

**Step 1:** Go to github `Setting->Developer setting->Personal access tokens (classic)->Generate new token(classic)` (**Note:** Make sure to copy your personal access token now. You won’t be able to see it again!)

With your token, connect your remote.

```sh
ssh mlops(replace it with yours)
```

```sh
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0
sudo apt-add-repository https://cli.github.com/packages
sudo apt update
sudo apt install gh
```

```sh
gh auth login
```
Follow the questions and finally paste your tokens as required.

**Note:** If you change to another computer, you have to regenerate a new token and `gh auth login` again 



