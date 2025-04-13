pipeline {
    agent any

    stages {
        stage('CHECKOUT') {
            steps {
                echo '📥 Cloning the repository...'
            }
        }

        stage('BUILD') {
            steps {
                echo '🔨 Building the Docker image...'
            }
        }

        stage('DEPLOY') {
            steps {
                echo '🚀 Deploying the container...'
            }
        }

        stage('TEST') {
            steps {
                echo '🧪 Testing the app status...'
            }
        }

        stage('PROMOTE') {
            steps {
                echo '✅ App is ready for production!'
            }
        }
    }
}
