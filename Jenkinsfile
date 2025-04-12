pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo '🔨 Building Docker Image...'
                sh 'docker build -t grocerystore-app .'
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying Container...'
                sh '''
                docker stop grocerystore-app || true
                docker rm grocerystore-app || true
                docker run -d \
                  -p 5000:5000 \
                  -v ${PWD}/products.db:/app/products.db \
                  --name grocerystore-app \
                  grocerystore-app
                '''
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Testing app status...'
                sh 'sleep 3' // Give the app time to start
                sh 'curl --fail http://localhost:5000 || exit 1'
            }
        }

        stage('Promote') {
            steps {
                echo '✅ Promote: App is ready for production!'
            }
        }
    }
}
