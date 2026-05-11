pipeline {

    agent any

    environment {
        SNOWFLAKE_ACCOUNT = credentials('SNOWFLAKE_ACCOUNT')
        SNOWFLAKE_USER = credentials('SNOWFLAKE_USER')
        SNOWFLAKE_PASSWORD = credentials('SNOWFLAKE_PASSWORD')
        SNOWFLAKE_ROLE = credentials('SNOWFLAKE_ROLE')
        SNOWFLAKE_DATABASE = credentials('SNOWFLAKE_DATABASE')
        SNOWFLAKE_WAREHOUSE = credentials('SNOWFLAKE_WAREHOUSE')
    }

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
                export DBT_PROFILES_DIR=$(pwd)
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