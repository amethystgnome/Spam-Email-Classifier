# 254FinalProject
## Create an Environment and Move to Working Directory

**macOS/Ubuntu:**

```bash
Python3 -m venv .venv
. .venv/bin/activate
```

**Windows:**
```bash
py -3 -m venv .venv

.venv\Scripts\activate
```

#install dependencies

pip install -r requirements.txt

#Create a mongodb local instance  
**Ubuntu**
```bash
    install curl and gnupg
    sudo apt-get install gnupg curl
```
get public key
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor

Create the /etc/apt/sources.list.d/mongodb-org-7.0.list file for Ubuntu 22.04 (Jammy): replace jammy with your version

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

reload local package base
sudo apt-get update

install lateset version of mongodb
sudo apt-get install -y mongodb-org

start mongodb process
sudo systemctl start mongod

verify
sudo systemctl status mongod

to stop mongodb
sudo systemctl stop mongod



