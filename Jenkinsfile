pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo '🔨 Building Docker Image...'
                sh '''
                    docker build -t grocerystore-app . || { echo "Docker build failed"; exit 1; }
                    docker images
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying Container...'
                sh '''
                    docker stop grocerystore-app || true
                    docker rm grocerystore-app || true
                    docker run -d -p 5000:5000 --name grocerystore-app grocerystore-app || {
                        echo "Docker run failed"
                        exit 1
                    }
                    docker ps
                '''
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Testing app status...'
                sh '''
                    sleep 10
                    curl --fail http://localhost:5000 || {
                        echo "Test failed"
                        exit 1
                    }
                '''
            }
        }

        stage('Promote') {
            steps {
                echo '✅ Promote: App is ready for production!'
            }
        }
    }
}
