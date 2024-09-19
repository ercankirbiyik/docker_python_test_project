pipeline {
    agent any

    parameters {
        string(name: 'Build_Name', defaultValue: 'Build_Name_1', description: 'Build adını girin')
        choice(name: 'node_count', choices: ['1', '2', '3', '4', '5'], description: 'Kaç tane Chrome Node çalıştırmak istersiniz?')
    }

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    echo "Preparing environment for Build: ${params.Build_Name}"
                    echo "Starting ${params.node_count} Chrome Nodes for the test"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo "Running tests with ${params.node_count} Chrome nodes"
                    sh "python3 run_tests.py ${params.node_count}"
                }
            }
        }

        stage('Send Test Results to Webhook') {
            steps {
                script {
                    echo "Sending test results to Webhook"
                    sh "curl -X POST -d 'results=Test Completed' https://webhook.site/5120da85-4b4d-4d06-9fe3-11f5eacfcc93"
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up Docker containers"
            sh "docker stop selenium-hub || true"
            sh "docker stop \$(docker ps -a -q --filter 'name=chrome-node-*') || true"
            sh "docker rm \$(docker ps -a -q --filter 'name=chrome-node-*') || true"
            echo "Build completed: ${params.Build_Name}"
        }
    }
}
