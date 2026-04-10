pipeline {
    agent any

    environment {
        IMAGE_NAME = "game-ci-cd"
        CONTAINER_NAME = "game-ci-cd-container"
        HOST_PORT = "8082"
        CONTAINER_PORT = "8000"
    }

    triggers {
        githubPush()
    }

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Pre-commit Sanity') {
            steps {
                sh '''
                . .venv/bin/activate
                pre-commit run --all-files
                '''
            }
        }

        stage('Unit Tests') {
   	    steps {
                sh '''
                . .venv/bin/activate
                export PYTHONPATH=$WORKSPACE
                pytest -q
                '''
           }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Container Smoke Test') {
            steps {
                sh '''
                docker rm -f ${CONTAINER_NAME}-smoke || true
                docker run -d --name ${CONTAINER_NAME}-smoke -p 9000:${CONTAINER_PORT} ${IMAGE_NAME}:latest
                sleep 5
                curl --fail http://localhost:9000/health
                docker rm -f ${CONTAINER_NAME}-smoke
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker rm -f ${CONTAINER_NAME} || true
                docker run -d \
                  --name ${CONTAINER_NAME} \
                  --restart unless-stopped \
                  -p ${HOST_PORT}:${CONTAINER_PORT} \
                  ${IMAGE_NAME}:latest
                '''
            }
        }
    }

    post {
        success {
            echo 'Build passed, deployed successfully.'
        }
        failure {
            echo 'Build failed. Deployment skipped.'
        }
        always {
            sh 'docker ps -a || true'
        }
    }
}
