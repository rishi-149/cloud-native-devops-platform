pipeline {
    agent any

    environment {
        IMAGE_NAME = "rishi1490/cloud-native-devops"
        IMAGE_TAG  = "${BUILD_NUMBER}"
        NAMESPACE  = "devops-platform"
        DEPLOYMENT = "cloud-native-devops"
        CONTAINER  = "cloud-native-devops"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Verify Tools') {
            steps {
                bat 'git --version'
                bat 'python --version'
                bat 'docker --version'
                bat 'kubectl version --client'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r app\\requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'pytest tests'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat """
                docker build ^
                -t %IMAGE_NAME%:%IMAGE_TAG% ^
                -t %IMAGE_NAME%:latest ^
                app
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    bat """
                    docker login -u %DOCKER_USER% -p %DOCKER_PASS%

                    docker push %IMAGE_NAME%:%IMAGE_TAG%
                    docker push %IMAGE_NAME%:latest

                    docker logout
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat """
                kubectl set image deployment/%DEPLOYMENT% ^
                %CONTAINER%=%IMAGE_NAME%:%IMAGE_TAG% ^
                -n %NAMESPACE%

                kubectl rollout status deployment/%DEPLOYMENT% -n %NAMESPACE%
                """
            }
        }

        stage('Verify Deployment') {
            steps {
                bat """
                kubectl get pods -n %NAMESPACE%
                kubectl get svc -n %NAMESPACE%
                """
            }
        }

        stage('Cleanup') {
            steps {
                bat """
                docker image rm %IMAGE_NAME%:%IMAGE_TAG% || exit /b 0
                docker image rm %IMAGE_NAME%:latest || exit /b 0
                """
            }
        }
    }

    post {

        success {
            echo "=============================================="
            echo "CI/CD Pipeline Completed Successfully!"
            echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
            echo "Deployment Updated Successfully"
            echo "=============================================="
        }

        failure {
            echo "=============================================="
            echo "Pipeline Failed!"
            echo "Check Jenkins Console Output"
            echo "=============================================="
        }

        always {
            cleanWs()
        }
    }
}