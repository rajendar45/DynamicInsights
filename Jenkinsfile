pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'python3 DynamicInsightsRestServcie.py'
            }
        }
        stage('Test') {
            steps {
                sh 'python3 -m unittest discover -s tests'
            }
        }
    }
}