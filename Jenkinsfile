pipeline {
  agent any
    stages {
        stage ('Build') {
            steps {
                sh '''#!/bin/bash
                python3.9 -m venv venv
                source venv/bin/activate
                pip install pip --upgrade
                pip install -r requirements.txt
		pip install gunicorn pymysql cryptography
		FLASK_APP=microblog.py
		flask translate compile
		flask db upgrade
                '''
            }
        }
        stage ('Test') {
            steps {
                sh '''#!/bin/bash
                source venv/bin/activate
                py.test ./tests/unit/ --verbose --junit-xml test-reports/results.xml
                '''
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
      stage ('OWASP FS SCAN') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
           }
        }
      stage ('Clean') {
            steps {
                sh '''#!/bin/bash
                if [[ $(ps aux | grep -i "gunicorn" | tr -s " " | head -n 1 | cut -d " " -f 2) != 0 ]]
                then
                ps aux | grep -i "gunicorn" | tr -s " " | head -n 1 | cut -d " " -f 2 > pid.txt
                kill $(cat pid.txt)
                exit 0
                fi
                '''
            }
        }
      stage ('Deploy') {
            steps {
                sh '''#!/bin/bash
                set -x  # Enable command echoing for debugging
                
                echo "Attempting to restart microblog service..."
                if sudo /bin/systemctl restart microblog; then
                    echo "Microblog service restarted successfully"
                else
                    echo "Failed to restart microblog service"
                    sudo /bin/systemctl status microblog || true
                    exit 1
                fi
                
                echo "Waiting for service to stabilize..."
                sleep 10
                
                echo "Checking service status..."
                if sudo /bin/systemctl is-active microblog; then
                    echo "Microblog service is active"
                    sudo /bin/systemctl status microblog || true
                else
                    echo "Microblog service failed to start"
                    sudo /bin/systemctl status microblog || true
                    exit 1
                fi
                '''
            }
        }
    }
}
