# Kura Labs Cohort 5- Deployment Workload 3


---

**Purpose**  
The purpose of this workload is to provision and deploy our own Infrastructure.

**Steps taken:** 

1. Create an Ubuntu EC2 instance (t3.medium) named “Jenkins”  
   1. Set Security Groups to SSH (Port 22\) and HTTP(Port 8080\)  
   2. Install Jenkins on server

sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins


2. Clone [this](https://github.com/kura-labs-org/C5-Deployment-Workload-3/tree/main) repo into your instance

3. Install Java

sudo apt update
sudo apt install fontconfig openjdk-17-jre
java -version
openjdk version "17.0.8" 2023-07-18
OpenJDK Runtime Environment (build 17.0.8+7-Debian-1deb12u1)
OpenJDK 64-Bit Server VM (build 17.0.8+7-Debian-1deb12u1, mixed mode, sharing)

4. Enable Jenkins
   sudo systemctl enable jenkins   
   sudo systemctl start jenkins   
   sudo systemctl status jenkins

If Jenkins is active, its now time to Git Clone [this](https://github.com/kura-labs-org/C5-Deployment-Workload-3/tree/main) repo to your instance.

5.   Install 'python3.9', 'python3.9-venv', 'python3-pip', and 'nginx'
To install Python 3.9   
   1. sudo add-apt-repository ppa:deadsnakes/ppa  
   2. sudo apt update  
   3. sudo apt install python3.9  
   4. Verify installation w/ python3.9 –version
sudo apt install python3.9 venv  
sudo apt install python3-pip  
sudo apt nginx

1. Make sure Nginx is installed using the following commands:  
   1. sudo systemctl enable nginx  
      2. sudo systemctl start nginx   
      3. sudo systemctl status nginx
Nginx should be active before moving on to the next step. 

3\. Activate virtual environment

1. cd into the directory that you cloned it should be “microblog\_EC2\_deployment”  
2. To activate the virtual environment, run the following command:   
   1. python3.9 \-m venv venv  
   2. source venv/bin/activate

4\. Install packages and dependencies 

1. pip install \-r requirements.txt  
2. pip install gunicorn pymysql cryptography

Inside of the terminal, set the environmental variable. Do not cd into another directory. 

FLASK_APP=microblog.py

6. Run the following commands:

flask translate compile  
flask db upgrade

7.Edit the NginX configuration file at "/etc/nginx/sites-enabled/default" so that "location" reads as below:

location / {  
proxy\_pass http://127.0.0.1:5000;  
proxy\_set\_header Host $host;  
proxy\_set\_header X-Forwarded-For $proxy\_add\_x\_forwarded\_for;  
}

8. Run the following command and then put the servers public IP address into the browser address bar

gunicorn \-b :5000 \-w 4 microblog:app

Automating Pipeline

1. Modify JenkinsFile and add the build and Deploy stage   
2. Add the following to the build stage of your Jenkins File:

                python3.9 \-m venv venv  
                source venv/bin/activate  
                pip install pip \--upgrade  
                pip install \-r requirements.txt  
		pip install gunicorn pymysql cryptography  
		FLASK\_APP=microblog.py  
		flask translate compile  
		flask db upgrade

3. Create a python script called test\_app.py to run a unit test of the application source code. IMPORTANT: Put the script in a directory called "tests/unit/" of the GitHub repository  
4. Write unit test:  
   1. Add the following imports:  
        
      import pytest  
      import sys  
      import os  
      sys.path.append(os.getcwd())  
      from microblog import app  
        
   2. Add functions to test application. The following tests the website home route

   
@pytest.fixture  
def client():  
    app.config.update({"TESTING": True,})  
    return app.test\_client()

def test\_website(client):  
    response \= client.get("/", follow\_redirects \= True)  
    assert response.status\_code \== 200
