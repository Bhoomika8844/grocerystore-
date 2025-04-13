pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo '🔨 Building the Docker image...'
                sh 'docker build -t grocerystore .'
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying the container...'

                // Remove existing container with the same name (if any)
                sh 'docker rm -f grocerystore || true'

                // Run the new container on port 8090
                sh 'docker run -d --name grocerystore -p 8090:80 grocerystore'
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running unit tests...'
                sh '''
                docker exec grocerystore python3 -m unittest discover -s tests -p "*.py"
                '''
            }
        }

        stage('Promote') {
            steps {
                echo '✅ App is ready for production on port 8090!'
            }
        }

        stage('Cleanup') {
            steps {
                echo '🧹 Cleaning up the container...'
                sh 'docker stop grocerystore || true'
                sh 'docker rm grocerystore || true'
            }
        }
    }
}
