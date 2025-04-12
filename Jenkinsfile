pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t grocerystore-app .'
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                docker stop grocerystore-app || true
                docker run -d \
                  -p 5000:5000 \
                  -v ${PWD}/products.db:/app/products.db \
                  --name grocerystore-app \
                  grocerystore-app
                '''
            }
        }
    }
}