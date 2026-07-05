pipeline {
    agent any
    environment {
        IMAGE_NAME = "riuu1110/aws-cost-optimizer"
        IMAGE_TAG  = "latest"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Riya-te/aws-cost-optimization.git'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv venv

                . venv/bin/activate

                pip install --upgrade pip

                pip install -r requirements.txt
                '''
            }
        }

        stage('Run AWS Cost Optimizer') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {

                    sh '''
                    . venv/bin/activate

                    python test.py
                    '''
                }
            }
        }

        stage('SonarQube Scan') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                
                withSonarQubeEnv('SonarQube') {
                    sh """
                     ${scannerHome}/bin/sonar-scanner
                    """
                }
              }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh """
                trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Push Docker Image') {
            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {

                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                    docker push ${IMAGE_NAME}:${IMAGE_TAG}

                    docker logout
                    '''
                }
            }
        }
         stage('Deploy Lambda') {
           steps {

             withCredentials([[
               $class: 'AmazonWebServicesCredentialsBinding',
               credentialsId: 'aws-creds'
        ]]) {

            sh '''
            echo "Creating deployment package..."

            rm -f deployment.zip

            zip -r deployment.zip . \
                -x "venv/*" \
                   ".git/*" \
                   "__pycache__/*" \
                   "*.pyc"

            echo "Updating Lambda..."

            aws lambda update-function-code \
                --function-name aws-cost-optimizer \
                --zip-file fileb://deployment.zip \
                --region ap-south-1
            '''
        }
    }
}
    }

    post {

        success {
            echo "========================================="
            echo "Pipeline Completed Successfully"
            echo "SonarQube Scan Completed"
            echo "Trivy Scan Completed"
            echo "Docker Image: ${IMAGE_NAME}:${IMAGE_TAG}"
            echo "========================================="
        }

        failure {
            echo "========================================="
            echo "Pipeline Failed"
            echo "========================================="
        }

        always {
            cleanWs()
        }
    }
}