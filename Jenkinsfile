pipeline {
    agent any

    environment {
        ALLURE_RESULTS = "allure-results"
        SCREENSHOTS = "screenshots"
        DOCKER_IMAGE = "selenium-tests:latest"
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
                bat 'docker build -t selenium-tests:latest -f "C:\\qaRoad\\my_selenium_test\\Dockerfile" "C:\\qaRoad\\my_selenium_test"'
            }
        }


        stage('Run UI Tests in Docker') {
            steps {
                echo 'Запуск UI тестов внутри Docker'
                dir("${env.WORKSPACE}") {
                    bat """
                    docker run --rm ^
                        -v %CD%\\${ALLURE_RESULTS}:/app/${ALLURE_RESULTS} ^
                        -v %CD%\\${SCREENSHOTS}:/app/${SCREENSHOTS} ^
                        ${DOCKER_IMAGE} ^
                        pytest --alluredir=${ALLURE_RESULTS}
                    """
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Генерация Allure отчета'
                dir("${env.WORKSPACE}") {
                    bat "allure generate ${ALLURE_RESULTS} -o allure-report --clean"
                }
            }
        }

        stage('Publish Report') {
            steps {
                echo 'Публикация HTML отчета в Jenkins'
                dir("${env.WORKSPACE}") {
                    bat "if not exist public mkdir public"
                    bat "xcopy /E /I /Y allure-report public\\"
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'public',
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
            echo 'Пайплайн завершился с ошибкой'
        }
    }
}
