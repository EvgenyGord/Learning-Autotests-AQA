pipeline {
    agent any

    environment {
        ALLURE_RESULTS = "allure-results"
        SCREENSHOTS = "screenshots"
        PUBLIC_REPORT = "public"
    }

    stages {

        stage('Preparation') {
            steps {
                echo 'Подготовка директорий для отчетов и скриншотов'
                bat "if not exist ${env.ALLURE_RESULTS} mkdir ${env.ALLURE_RESULTS}"
                bat "if not exist ${env.SCREENSHOTS} mkdir ${env.SCREENSHOTS}"
            }
        }

        stage('Prepare Dockerfile') {
            steps {
                echo 'Копирование Dockerfile в workspace Jenkins'
                // Если Dockerfile в корне репозитория, этот шаг можно убрать
                // Иначе путь нужно указать реальный
                bat 'copy Dockerfile .'
            }
        }

        stage('UI Tests in Docker') {
            steps {
                echo 'Сборка Docker образа для тестов'
                bat 'docker build -t selenium-tests:latest .'

                echo 'Запуск тестов в Docker контейнере'
                bat """
                    docker run --name selenium-test-container-${BUILD_ID} -v %cd%\\${env.ALLURE_RESULTS}:/app/${env.ALLURE_RESULTS} selenium-tests:latest
                """
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Генерация Allure отчетов'
                bat "allure generate ${env.ALLURE_RESULTS} -o allure-report --clean"
            }
        }

        stage('Publish Report') {
            steps {
                echo 'Публикация HTML отчета в Jenkins'
                bat "if not exist ${env.PUBLIC_REPORT} mkdir ${env.PUBLIC_REPORT}"
                bat "xcopy /E /I /Y allure-report ${env.PUBLIC_REPORT}\\"
                publishHTML(target: [
                    reportName: 'Test Report',
                    reportDir: env.PUBLIC_REPORT,
                    reportFiles: 'index.html',
                    keepAll: true,
                    alwaysLinkToLastBuild: true
                ])
            }
        }
    }

    post {
        always {
            echo 'Очистка ресурсов Docker'
            bat "docker rm -f selenium-test-container-${BUILD_ID} || echo \"Контейнеров нет\""
            bat "docker image prune -f || echo \"Нет неиспользуемых образов\""
        }
        success {
            echo 'Пайплайн успешно завершён'
        }
        failure {
            echo 'Пайплайн завершился с ошибками'
        }
    }
}
