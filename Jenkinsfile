pipeline {
    agent any

    environment {
        ALLURE_RESULTS = "allure-results"
        SCREENSHOTS = "screenshots"
        DOCKER_IMAGE = "selenium-tests:latest"
        PROJECT_DIR = "C:\\qaRoad\\my_selenium_test"
        TARGET_URL = "http://31.59.174.108"
        REPORT_DIR = "build\\reports\\allure"    // путь для Jenkins
    }

    stages {

        stage('Preparation') {
            steps {
                echo '📁 Подготовка директорий для отчетов и скриншотов'
                bat "if not exist ${ALLURE_RESULTS} mkdir ${ALLURE_RESULTS}"
                bat "if not exist ${SCREENSHOTS} mkdir ${SCREENSHOTS}"
                bat "if not exist ${REPORT_DIR} mkdir ${REPORT_DIR}"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Сборка Docker образа для тестов'
                bat "docker build -t ${DOCKER_IMAGE} -f \"${PROJECT_DIR}\\Dockerfile\" \"${PROJECT_DIR}\""
            }
        }

        stage('Check Target Availability') {
            steps {
                echo "🌐 Проверка доступности сайта: ${TARGET_URL}"
                script {
                    def result = bat(script: "curl -I ${TARGET_URL}", returnStatus: true)
                    if (result != 0) {
                        echo "⚠️ Сайт ${TARGET_URL} недоступен. Тесты могут упасть."
                    } else {
                        echo "✅ Сайт ${TARGET_URL} доступен."
                    }
                }
            }
        }

        stage('Run UI Tests in Docker') {
            steps {
                echo '🧪 Запуск UI тестов внутри Docker'
                script {
                    catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                        bat """
                        docker run --rm ^
                            -v "${PROJECT_DIR}\\${ALLURE_RESULTS}:/app/${ALLURE_RESULTS}" ^
                            -v "${PROJECT_DIR}\\${SCREENSHOTS}:/app/${SCREENSHOTS}" ^
                            ${DOCKER_IMAGE} ^
                            pytest --alluredir=/app/${ALLURE_RESULTS}
                        """
                    }
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo '📊 Генерация Allure отчета'
                script {
                    catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                        bat "allure generate ${PROJECT_DIR}\\${ALLURE_RESULTS} -o ${PROJECT_DIR}\\${REPORT_DIR} --clean"
                    }
                }
            }
        }
    }

    post {
        success {
            echo '📢 Публикация Allure отчета'
            script {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: "${PROJECT_DIR}\\${REPORT_DIR}",
                    reportFiles: 'index.html',
                    reportName: '🧾 Allure Report'
                ])
                echo "✅ Отчёт доступен по ссылке: ${env.BUILD_URL}Allure_20Report/"
            }
        }

        always {
            echo '🧹 Очистка Docker-ресурсов'
            bat "docker container prune -f || echo 'Нет контейнеров для удаления'"
            bat "docker image prune -f || echo 'Нет неиспользуемых образов'"
        }

        failure {
            echo '❌ Пайплайн завершился с ошибкой, отчёт всё равно сгенерирован (если возможно).'
        }
    }
}
