pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = "1"
        ALLURE_RESULTS_DIR = "allure-results"
        ALLURE_REPORT_DIR = "allure-report"
    }

    stages {
        stage('Preparation') {
            steps {
                script {
                    echo "Подготовка директорий для отчетов и скриншотов"
                    bat '''
                        if not exist allure-results mkdir allure-results
                        if not exist screenshots mkdir screenshots
                    '''
                    bat "docker info || echo Docker недоступен"
                }
            }
        }

        stage('UI Tests in Docker') {
            steps {
                script {
                    echo "Сборка Docker образа для тестов"
                    try {
                        def testImage = docker.build("selenium-tests:${env.BUILD_ID}", ".")
                        echo "Запуск тестов в контейнере"
                        testImage.run(
                            "--name selenium-test-container-${env.BUILD_ID} " +
                            "-v ${WORKSPACE}\\allure-results:/app/allure-results " +
                            "-v ${WORKSPACE}\\screenshots:/app/screenshots " +
                            "--rm"
                        )
                    } catch (Exception e) {
                        echo "Тесты завершились с ошибками: ${e.getMessage()}"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'allure-results/**/*', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'screenshots/**/*', allowEmptyArchive: true
                }
            }
        }

        stage('Generate Allure Reports') {
            steps {
                script {
                    echo "Генерация Allure отчетов"
                    try {
                        bat "allure generate allure-results -o allure-report --clean"
                    } catch (Exception e) {
                        echo "Ошибка генерации Allure отчета: ${e.getMessage()}"
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'allure-report/**/*', allowEmptyArchive: true
                }
            }
        }

        stage('Publish Report') {
            steps {
                script {
                    echo "Публикация HTML отчета в Jenkins"
                    bat '''
                        if not exist public mkdir public
                        xcopy /E /I /Y allure-report public\\
                    '''
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'public',
                        reportFiles: 'index.html',
                        reportName: 'Test Report',
                        reportTitles: 'Отчет по автотестам'
                    ])
                }
            }
        }
    }

    post {
        always {
            echo "Очистка ресурсов Docker"
            bat '''
                docker rm -f selenium-test-container-${BUILD_ID} || echo "Контейнеров нет"
                docker image prune -f || echo "Нет неиспользуемых образов"
            '''
        }
        success { echo "Пайплайн выполнен успешно!" }
        failure { echo "Пайплайн завершился с ошибками" }
        unstable { echo "Пайплайн завершился с предупреждениями" }
    }
}
