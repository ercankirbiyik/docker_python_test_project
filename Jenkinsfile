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
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Testlerin maksimum 10 dakika içinde bitmesi için timeout mekanizması
                    timeout(time: 10, unit: 'MINUTES') {
                        echo "Running tests with ${params.node_count} Chrome nodes"
                        // Sanal ortam üzerinden testleri çalıştırma
                        sh "./venv/bin/python3 run_tests.py ${params.node_count}"
                    }
                }
            }
        }

        stage('Send Test Results to Webhook') {
            steps {
                script {
                    echo "Sending test results to Webhook"
                    def status = currentBuild.result ?: 'SUCCESS'

                    sh """
                    curl -X POST -H "Content-Type: application/json" -d '{
                        "build_name": "${params.Build_Name}",
                        "node_count": "${params.node_count}",
                        "status": "${status}"
                    }' https://webhook.site/b8f12633-2a84-4e1c-9950-a76fa8ab8c66
                    """
                }
            }
        }

        stage('Clean Old Builds') {
            steps {
                script {
                    echo "Cleaning up old builds, keeping only the last 5..."
                    // Son 5 build dışındaki tüm build'leri temizleme
                    sh '''
                    cd /var/lib/jenkins/jobs/${JOB_NAME}/builds
                    ls -1t | tail -n +6 | xargs rm -rf
                    '''
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
