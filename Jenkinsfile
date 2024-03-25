pipeline {
    agent any
    stages {
        stage('git-checkout') {
            steps {
                checkout([$class: 'GitSCM',
                          branches: [[name: '*/main']],
                          userRemoteConfigs: [[url: 'https://github.com/galrazabi/AIBrandDesginer']]])
            }
        }

        stage('build docker image'){
        steps{
            sh 'docker build -t aibranddesigner.azurecr.io/aibranddesigner:latest .'
        }
    }
    stage('push image'){
        steps{
            withCredentials([usernamePassword(credentialsId: 'ACR', passwordVariable: 'password', usernameVariable: 'username')]) {
            sh 'docker login -u ${username} -p ${password} aibranddesigner.azurecr.io'
            sh 'docker push aibranddesigner.azurecr.io/aibranddesigner:latest'
            }
            }
        }

    stage('install Azure CLI'){
        steps{
            sh '''
            brew update
            brew install azure-cli
            '''
        }
    }

    stage('deploy web-app'){
        steps{
            withCredentials([azureServicePrincipal('azureServicePrincipal')]) {
            sh 'az login --service-principal -u ${AZURE_CLIENT_ID} -p ${AZURE_CLIENT_SECRET} --tenant ${AZURE_TENANT_ID}'
            }
            withCredentials([usernamePassword(credentialsId: 'ACR', passwordVariable: 'password', usernameVariable: 'username')]) {
            sh 'az webapp config container set --name aibranddesigner --resource-group rg-branddesigner --docker-custom-image-name aibranddesigner.azurecr.io/aibranddesigner:latest --docker-registry-server-url https://aibranddesigner.azurecr.io --docker-registry-server-user ${username} --docker-registry-server-password ${password}'
            }
        }
    }
    }
}
