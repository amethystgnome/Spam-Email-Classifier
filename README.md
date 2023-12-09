# 254FinalProject
## Creating venv for python
----

**macOS:**

```bash
Python3 -m venv .venv
```
```bash 
. .venv/bin/activate
```
**Ubuntu**
```bash 
sudo apt install --yes python3-pip python3-venv
```
```bash 
python3.10 -m venv $HOME/.venv
echo 'source $HOME/.venv/bin/activate' | tee -a $HOME/.bashrc
. $HOME/.venv/bin/activate
```



# Install dependencies
---
```bash
pip install -r requirements.txt
```

# *Create a mongodb local instance*
---
## Linux/Windows
Install mongodb community server msi at https://www.mongodb.com/try/download/community
##  **Ubuntu**
### install curl and gnupg
```bash
    sudo apt-get install gnupg curl
```
### get public key
```bash
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
```
###Create the /etc/apt/sources.list.d/mongodb-org-7.0.list file for Ubuntu 22.04 (Jammy): replace jammy with your version

```bash
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```
### reload local package base
```bash 
sudo apt-get update
```
### install lateset version of mongodb
```bash 
sudo apt-get install -y mongodb-org
```
### start mongodb process
 ```bash 
 sudo systemctl start mongod
```
### verify
```bash 
sudo systemctl status mongod
```

### to stop mongodb
```bash
sudo systemctl stop mongod
```



# Starting flask app
---
```bash
flask --app index run
```

