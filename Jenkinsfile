pipeline {

    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Validate Python') {
            steps {
                sh 'python3 -m py_compile etl/extract/*.py'
            }
        }

        stage('dbt Tests') {
            steps {
                sh '''
                cd retail_dbt
                dbt test
                '''
            }
        }

        stage('Airflow DAG Validation') {
            steps {
                sh '''
                docker exec airflow-webserver airflow dags list
                '''
            }
        }
    }
}