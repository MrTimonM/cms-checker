@echo off

set /p "REPO_NAME=Enter the repository name: "

:: Initialize Git repository
git init
ping 127.0.0.1 -n 2 > nul   :: Delay for 2 seconds

:: Add all files
git add .
ping 127.0.0.1 -n 2 > nul   :: Delay for 2 seconds

:: Commit the changes
git commit -m "Initial commit"
ping 127.0.0.1 -n 2 > nul   :: Delay for 2 seconds

:: Create the private repository on GitHub using GitHub CLI
gh repo create %REPO_NAME% --private
ping 127.0.0.1 -n 2 > nul   :: Delay for 2 seconds

:: Push the code to the remote repository
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/%REPO_NAME%.git
git push -u origin master

pause
