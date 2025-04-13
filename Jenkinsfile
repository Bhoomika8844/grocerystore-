pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo '🔨 Building the Docker image...'
                sh 'docker build -t grocerystore .'
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying the container...'
                sh 'docker rm -f grocerystore || true'
                sh 'docker run -d --name grocerystore -p 8090:5000 grocerystore'
                sleep time: 5, unit: 'SECONDS' // Wait for Flask to start
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running unit tests...'
                sh 'docker exec grocerystore python3 -m unittest discover -s tests -p "*.py"'
            }
        }
    }
}
