pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "selenium-tests:latest"
        WORKSPACE_DIR = "${env.WORKSPACE}"
    }

    stages {
        stage('Preparation') {
            steps {
                echo 'Подготовка директорий для отчетов и скриншотов'
                bat 'if not exist allure-results mkdir allure-results'
                bat 'if not exist screenshots mkdir screenshots'
            }
        }

        stage('UI Tests in Docker') {
            steps {
                script {
                    echo 'Сборка Docker образа для тестов'

                    // Собираем Docker образ
                    bat "docker build -t ${DOCKER_IMAGE} ."

                    echo 'Запуск тестов в контейнере'
                    // Запуск контейнера с монтированием текущей папки
                    bat """
                    docker run --rm ^
                    -v ${WORKSPACE_DIR}\\allure-results:/app/allure-results ^
                    -v ${WORKSPACE_DIR}\\screenshots:/app/screenshots ^
                    ${DOCKER_IMAGE}
                    """
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Генерация Allure отчетов'
                bat 'allure generate allure-results -o allure-report --clean'
            }
        }

        stage('Publish Report') {
            steps {
                echo 'Публикация HTML отчета в Jenkins'
                bat 'if not exist public mkdir public'
                bat 'xcopy /E /I /Y allure-report public\\'
                publishHTML(target: [
                    reportDir: 'public',
                    reportFiles: 'index.html',
                    reportName: 'Test Report'
                ])
            }
        }
    }

    post {
        always {
            echo 'Очистка ресурсов Docker'
            bat 'docker container prune -f || echo "Нет контейнеров для удаления"'
            bat 'docker image prune -f || echo "Нет неиспользуемых образов"'
        }
    }
}
