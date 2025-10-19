pipeline {
    agent any

    environment {
        ALLURE_RESULTS = "allure-results"
        SCREENSHOTS = "screenshots"
        DOCKER_IMAGE = "selenium-tests:latest"
        PROJECT_DIR = "C:\\qaRoad\\my_selenium_test"
        TARGET_URL = "http://31.59.174.108"
        TEST_DIR = "tests" // папка с тестами внутри проекта
    }

    stages {

        stage('Preparation') {
            steps {
                echo '📁 Подготовка директорий для отчетов и скриншотов'
                bat "if not exist ${ALLURE_RESULTS} mkdir ${ALLURE_RESULTS}"
                bat "if not exist ${SCREENSHOTS} mkdir ${SCREENSHOTS}"
            }
        }

        stage('Copy Dockerfile to Workspace') {
            steps {
                echo '📄 Копирование Dockerfile в workspace'
                bat "copy /Y \"${PROJECT_DIR}\\Dockerfile\" \"%WORKSPACE%\\Dockerfile\""
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Сборка Docker образа для тестов'
                bat "docker build -t ${DOCKER_IMAGE} -f \"%WORKSPACE%\\Dockerfile\" \"%WORKSPACE%\""
            }
        }

        stage('Check Target Availability') {
            steps {
                echo "🌐 Проверка доступности сайта: ${TARGET_URL}"
                script {
                    def result = bat(script: "curl -I ${TARGET_URL}", returnStatus: true)
                    if (result != 0) {
                        echo "⚠️ Внимание: сайт ${TARGET_URL} недоступен. Проверка пропущена."
                    } else {
                        echo "✅ Сайт ${TARGET_URL} доступен."
                    }
                }
            }
        }

        stage('Run Tests in Docker') {
            steps {
                echo '🧪 Запуск тестов внутри Docker'
                script {
                    catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                        bat """
                        docker run --rm ^
                            -v "%WORKSPACE%\\${ALLURE_RESULTS}:/app/${ALLURE_RESULTS}" ^
                            -v "%WORKSPACE%\\${SCREENSHOTS}:/app/${SCREENSHOTS}" ^
                            -v "${PROJECT_DIR}\\${TEST_DIR}:/app/${TEST_DIR}" ^
                            ${DOCKER_IMAGE} ^
                            pytest /app/${TEST_DIR} --alluredir=/app/${ALLURE_RESULTS}
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
                        bat "allure generate %WORKSPACE%\\${ALLURE_RESULTS} -o %WORKSPACE%\\allure-report --clean"
                    }
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                echo '📢 Публикация Allure отчета через Allure Jenkins Plugin'
                allure([
                    includeProperties: false,
                    jdk: '',
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: "${ALLURE_RESULTS}"]]
                ])
            }
        }
    }

    post {
        always {
            echo '🧹 Очистка ресурсов Docker'
            bat "docker container prune -f || echo 'Нет контейнеров для удаления'"
            bat "docker image prune -f || echo 'Нет неиспользуемых образов'"
        }
        success {
            echo "✅ Пайплайн завершён успешно! Allure Report доступен на боковой панели Jenkins."
        }
        unstable {
            echo "⚠️ Пайплайн завершён с предупреждениями, но отчёт Allure доступен."
        }
        failure {
            echo "❌ Пайплайн завершился с ошибкой, проверь логи."
        }
    }
}
