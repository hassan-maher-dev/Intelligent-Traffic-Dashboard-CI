pipeline {
    agent any
    environment {
        DOCKERHUB_USER = "hassanmaher2001" 
        DASHBOARD_IMG = "traffic-dashboard"
        COLLECTOR_IMG = "traffic-collector"
        IMAGE_TAG = "${env.BUILD_ID}"
        GITOPS_REPO = "github.com/hassan-maher-dev/notes-app-gitops.git" // Change the repo name if you created a new one
    }

    stages {
        stage('Build Docker Images') {
            steps {
                echo "Building Dashboard & Collector images..."
                dir('dashboard') {
                    sh "docker build -t ${DOCKERHUB_USER}/${DASHBOARD_IMG}:${IMAGE_TAG} ."
                }
                dir('collector') {
                    sh "docker build -t ${DOCKERHUB_USER}/${COLLECTOR_IMG}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                    
                    sh "docker push ${DOCKERHUB_USER}/${DASHBOARD_IMG}:${IMAGE_TAG}"
                    sh "docker push ${DOCKERHUB_USER}/${COLLECTOR_IMG}:${IMAGE_TAG}"
                }
            }
        }

        stage('Update GitOps Manifests') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-token', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                    sh '''
                        git clone https://$GIT_USERNAME:$GIT_PASSWORD@${GITOPS_REPO}
                        cd notes-app-gitops # Make sure the GitOps folder name is correct

                        git config user.email "jenkins@devops.com"
                        git config user.name "Jenkins CI"

                        # Update the tags for both services
                        sed -i "s|image: ${DOCKERHUB_USER}/${DASHBOARD_IMG}:.*|image: ${DOCKERHUB_USER}/${DASHBOARD_IMG}:${IMAGE_TAG}|g" deployment-dashboard.yaml
                        sed -i "s|image: ${DOCKERHUB_USER}/${COLLECTOR_IMG}:.*|image: ${DOCKERHUB_USER}/${COLLECTOR_IMG}:${IMAGE_TAG}|g" deployment-collector.yaml

                        git add deployment-dashboard.yaml deployment-collector.yaml
                        git commit -m "Auto-update images to build ${IMAGE_TAG}"
                        git push origin main
                    '''
                }
            }
        }
    }
   post {
        always {
            echo "Cleaning up workspace and local Docker images..."
            sh "docker rmi ${DOCKERHUB_USER}/${DASHBOARD_IMG}:${IMAGE_TAG} || true"
            sh "docker rmi ${DOCKERHUB_USER}/${COLLECTOR_IMG}:${IMAGE_TAG} || true"
            deleteDir()
        }
        success {
            echo "✅ SUCCESS: The images were built, pushed, and GitOps repo is updated!"
            // In the future, you can add code here to send a success notification to Slack or Teams.
        }
        failure {
            echo "❌ FAILED: Something went wrong during the pipeline execution."
            // In the future, you can add code here to send a failure alert email.
        }
    }
}