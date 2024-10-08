pipeline {
    agent any

    parameters {
        string(name: 'Build_Name', defaultValue: 'qa_manuel', description: 'Build adını girin')
        choice(name: 'node_count', choices: ['1', '2', '3', '4', '5'], description: 'Kaç tane Chrome Node çalıştırmak istersiniz?')
    }

    stages {
        stage('Install Python & Docker module') {
            steps {
                script {
                    // Python, pip ve venv modülünün yüklü olup olmadığını kontrol etme
                    sh 'sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv'

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

                    // Aynı isimdeki konteyneri kaldırma
                    for (int i = 1; i <= params.node_count.toInteger(); i++) {
                        def containerId = sh(script: "docker ps -a -q --filter name=chrome-node-${i}", returnStdout: true).trim()
                        if (containerId) {
                            echo "Stopping and removing existing chrome-node-${i} container..."
                            sh "docker stop ${containerId}"
                            sh "docker rm ${containerId}"
                        }
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Testlerin maksimum 15 dakika içinde bitmesi için timeout mekanizması
                    timeout(time: 15, unit: 'MINUTES') {
                        echo "Running tests with ${params.node_count} Chrome nodes"
                        // Sanal ortam üzerinden testleri çalıştırma
                        sh "./venv/bin/python3 run_tests.py ${params.node_count}"
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                // Sonucu elde etme
                def status = 'SUCCESS'
                if (currentBuild.result == 'FAILURE') {
                    status = 'FAILURE'
                } else if (currentBuild.result == 'ABORTED') {
                    status = 'ABORTED'
                } else if (currentBuild.result == 'UNSTABLE') {
                    status = 'UNSTABLE'
                } else if (currentBuild.result == 'TIMEOUT') {
                    status = 'TIMEOUT'
                }

                // Sonuçları webhook'a gönderme
                echo "Sending test results to Webhook with status: ${status}"

                sh """
                curl -X POST -H "Content-Type: application/json" -d '{
                    "build_name": "${params.Build_Name}",
                    "node_count": "${params.node_count}",
                    "status": "${status}"
                }' https://webhook.site/b8f12633-2a84-4e1c-9950-a76fa8ab8c66
                """

                // Docker konteynerlerini temizleme
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
