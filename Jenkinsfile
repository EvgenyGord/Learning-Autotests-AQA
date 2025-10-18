pipeline {
    agent any

    environment {
        ALLURE_RESULTS = "allure-results"
        SCREENSHOTS = "screenshots"
        DOCKER_IMAGE = "selenium-tests:latest"
        PROJECT_DIR = "C:\\qaRoad\\my_selenium_test"
    }

    stages {

        stage('Preparation') {
            steps {
                echo 'Подготовка директорий для отчетов и скриншотов'
                bat "if not exist ${ALLURE_RESULTS} mkdir ${ALLURE_RESULTS}"
                bat "if not exist ${SCREENSHOTS} mkdir ${SCREENSHOTS}"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Сборка Docker образа для тестов'
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    bat "docker build -t ${DOCKER_IMAGE} -f \"${PROJECT_DIR}\\Dockerfile\" \"${PROJECT_DIR}\""
                }
            }
        }

        stage('Run UI Tests in Docker') {
            steps {
                echo 'Запуск UI тестов внутри Docker (ошибки не останавливают процесс)'
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    bat """
                    docker run --rm ^
                        -v \"${PROJECT_DIR}\\${ALLURE_RESULTS}:/app/${ALLURE_RESULTS}\" ^
                        -v \"${PROJECT_DIR}\\${SCREENSHOTS}:/app/${SCREENSHOTS}\" ^
                        ${DOCKER_IMAGE} ^
                        pytest --alluredir=/app/${ALLURE_RESULTS} || exit 0
                    """
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Генерация Allure отчета (даже при ошибках тестов)'
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    bat "allure generate ${PROJECT_DIR}\\${ALLURE_RESULTS} -o ${PROJECT_DIR}\\allure-report --clean || echo Allure report generation failed"
                }
            }
        }

        stage('Publish Report') {
            steps {
                echo 'Публикация HTML отчета в Jenkins'
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    bat "if not exist ${PROJECT_DIR}\\public mkdir ${PROJECT_DIR}\\public"
                    bat "xcopy /E /I /Y ${PROJECT_DIR}\\allure-report ${PROJECT_DIR}\\public\\"
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: "${PROJECT_DIR}\\public",
                        reportFiles: 'index.html',
                        reportName: 'Allure Report'
                    ])
                }
            }
        }
    }

    post {
        always {
            echo 'Очистка ресурсов Docker'
            bat "docker container prune -f || echo 'Нет контейнеров для удаления'"
            bat "docker image prune -f || echo 'Нет неиспользуемых образов'"
        }
        failure {
            echo 'Пайплайн завершился с ошибками, но отчёт сгенерирован.'
        }
        success {
            echo 'Пайплайн успешно завершён.'
        }
    }
}
