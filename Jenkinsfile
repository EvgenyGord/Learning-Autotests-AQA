pipeline {
    agent any
    environment {
        ALLURE_RESULTS = "${WORKSPACE}/allure-results"
        SCREENSHOTS = "${WORKSPACE}/screenshots"
    }
    stages {
        stage('Preparation') {
            steps {
                echo 'Подготовка директорий для отчетов и скриншотов'
                bat 'if not exist allure-results mkdir allure-results'
                bat 'if not exist screenshots mkdir screenshots'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Сборка Docker образа для тестов'
                bat 'docker build -t selenium-tests:latest .'
            }
        }

        stage('Run UI Tests in Docker') {
            steps {
                echo 'Запуск UI тестов внутри Docker'
                bat '''
                    docker run --rm ^
                        -v "%ALLURE_RESULTS%:/app/allure-results" ^
                        -v "%SCREENSHOTS%:/app/screenshots" ^
                        selenium-tests:latest
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo 'Генерация отчета Allure'
                bat 'allure generate allure-results --clean -o allure-report'
            }
        }

        stage('Publish Report') {
            steps {
                echo 'Публикация отчета Allure'
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
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
