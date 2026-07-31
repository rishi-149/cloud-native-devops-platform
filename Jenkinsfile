pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Git') {
            steps {
                bat 'git --version'
            }
        }

        stage('Verify Python') {
            steps {
                bat 'python --version'
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
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}