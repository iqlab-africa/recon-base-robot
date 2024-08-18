#!/bin/bash
# 🔴 🔴 Parameters provided (should be in this order):
# 🔴 SSH Key Path: /Users/aubreymalabie/.ssh/i_account2 - this is where ssgen has put your key. this is the key to be installed on GitHub console
# 🔴 Repository SSH URL: git@github.com:iqlab-africa/starter-example.git - this is the SSH url and NOT the normal https - You get this by clicking Get Code on the console
# 🔴 Commit Message: refactored push script 👿
# 🍎🍎🍎🍎 COMMAND TO PUSH CODE
#  ./push.sh ~/.ssh/i_account2 git@github.com:iqlab-africa/starter-backend.git "🔵 initial commit"


echo "🔴 🔴 🔴 🔴 🔴 Generic GitHub Push script starting ..."
echo "🔴 🔴 🔴"

# Ensure the script is called with three arguments
if [ "$#" -ne 3 ]; then
  echo "👿 Please enter required parameters: SSH key path, repository SSH URL and commit message. 👿"
  exit 1
fi

# Assign parameters to variables
ssh_key_path=$1
repository_ssh_url=$2
commit_message=$3

# Echo the parameters for clarity
echo "🔴 🔴 Parameters provided:"
echo "🔴 SSH Key Path: $ssh_key_path"
echo "🔴 Repository SSH URL: $repository_ssh_url"
echo "🔴 Commit Message: $commit_message"

# Check if SSH key path file exists
if [ ! -f "$ssh_key_path" ]; then
  echo "👿 SSH key file does not exist at the specified path: $ssh_key_path 👿"
  exit 1
fi

# Check if the repository SSH URL is valid (basic check)
if ! echo "$repository_ssh_url" | grep -q "^git@github.com:.*\.git$"; then
  echo "👿 Repository SSH URL does not seem valid: $repository_ssh_url 👿"
  exit 1
fi

# Set up SSH and check connection
echo "🎽🎽🎽🎽 Pulling the code ... using SSH Key ..."
eval "$(ssh-agent -s)"
ssh-add "$ssh_key_path" || { echo "👿 Failed to add SSH key. 👿"; exit 1; }
ssh -T git@github.com 

# Set the remote URL
echo "🍎 🍎 🍎 Setting remote SSH URL ... $2"
git remote set-url origin "$repository_ssh_url"

# Pull the code
echo "🍎 🍎 🍎 ... Pulling the code ..."
git pull || { echo "👿👿👿👿 Failed to pull code. 👿"; exit 1; }

echo "DONE!! 🥬 🥬 🥬 🥬 🥬 🥬 🥬 🥬 🥬 🥬 🥬"

