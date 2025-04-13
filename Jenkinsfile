pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Cloning the repository...'
                git 'https://github.com/Bhoomika8844/grocerystore.git'
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
                sh 'docker run -d -p 8080:80 grocerystore'
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running unit tests...'
                sh '''
                docker exec grocerystore python -m unittest discover -s tests -p "*.py"
                '''
            }
        }
    }
}
