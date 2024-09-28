pipeline {
    agent any

    parameters {
        string(name: 'Build_Name', defaultValue: 'Build_Name_1', description: 'Build adını girin')
        choice(name: 'node_count', choices: ['1', '2', '3', '4', '5'], description: 'Kaç tane Chrome Node çalıştırmak istersiniz?')
    }

    stages {
        stage('Install Python & Docker module') {
            steps {
                script {
                    // Python ve pip'in yüklü olup olmadığını kontrol etme
                    sh 'sudo apt-get update && sudo apt-get install -y python3 python3-pip'

                    // Sanal ortam oluşturma
                    echo "Setting up virtual environment"
                    sh "python3 -m venv venv"

                    // Sanal ortamı aktifleştirip pip'i güncelleme ve docker modülünü yükleme
                    sh "./venv/bin/pip install --upgrade pip"
                    sh "./venv/bin/pip install docker"
                }
            }
        }

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

                    // Sanal ortam üzerinden testleri çalıştırma
                    sh "./venv/bin/python3 run_tests.py ${params.node_count}"
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
            script {
                echo "Cleaning up Docker containers"

                def seleniumHub = sh(script: "docker ps -a -q --filter 'name=selenium-hub'", returnStdout: true).trim()
                if (seleniumHub) {
                    sh "docker stop ${seleniumHub}"
                    sh "docker rm ${seleniumHub}"
                }

                def chromeNodes = sh(script: "docker ps -a -q --filter 'name=chrome-node-*'", returnStdout: true).trim()
                if (chromeNodes) {
                    sh "docker stop ${chromeNodes}"
                    sh "docker rm ${chromeNodes}"
                }

                echo "Build completed: ${params.Build_Name}"
            }
        }
    }
}
