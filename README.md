# Retail Data Migration Project

## Overview

This project demonstrates how to migrate data from a legacy Microsoft SQL Server database into Snowflake using Python ETL pipelines, Apache Airflow orchestration, and dbt-powered warehouse transformations.

The platform simulates a modern cloud data engineering environment where transactional retail data is incrementally extracted from a legacy relational database, loaded into a cloud warehouse, transformed into analytics-ready models, validated through automated testing, and monitored through operational logging and alerting.

The project was designed to mirror real-world enterprise data platform architecture and operational workflows.

---

# Project Objectives

* Simulate a legacy retail transactional database
* Build modular Python ETL pipelines
* Implement incremental data loading strategies
* Load raw data into Snowflake
* Build analytics-ready warehouse models using dbt
* Implement automated data quality testing
* Orchestrate pipelines with Apache Airflow
* Add operational observability and audit logging
* Configure automated failure alerting
* Apply secure environment-driven configuration practices
* Prepare the platform for CI/CD automation

---

# Tech Stack

## Infrastructure

* Docker
* Docker Compose

## Databases & Warehousing

* Microsoft SQL Server
* Snowflake

## Data Engineering

* Python
* Pandas
* SQLAlchemy
* PyODBC

## Orchestration

* Apache Airflow

## Analytics Engineering

* dbt (data build tool)

## Data Quality & Governance

* dbt Tests

## Development Tools

* TablePlus
* Git
* GitHub

---

# High-Level Architecture

```text
                    +-------------------+
                    | Legacy SQL Server |
                    |   Retail System   |
                    +---------+---------+
                              |
                              |
                    Incremental ETL
                              |
                              v
                    +-------------------+
                    | Python ETL Layer  |
                    +---------+---------+
                              |
                              |
                              v
                    +-------------------+
                    |   Snowflake RAW   |
                    +---------+---------+
                              |
                              |
                              v
                    +-------------------+
                    |   dbt Models &    |
                    | Warehouse Layers  |
                    +---------+---------+
                              |
                              |
                              v
                    +-------------------+
                    | Analytics Models  |
                    +-------------------+

```

---

# Current Platform Features

## Legacy Database Simulation

The project includes a simulated retail transactional system built on Microsoft SQL Server.

### Tables

* customers
* stores
* products
* orders
* order_items
* inventory
* payments

### Synthetic Data Generation

* 1,000+ generated customer and order records
* Randomized retail transactions
* Timestamp-based incremental loading support

---

# ETL Pipelines

## Python Extraction Layer

The ETL layer is built using:

* Pandas
* SQLAlchemy
* Modular extraction scripts

### Features

* Modular extraction functions
* Reusable database connection layer
* CSV export support
* Incremental extraction support
* Parameterized SQL queries
* Environment-based configuration

---

# Incremental Loading

The platform implements stateful incremental loading using metadata watermark tracking.

## Metadata Tracking

A Snowflake metadata table stores:

* table_name
* last_loaded_timestamp

The ETL pipeline:

1. Reads the latest watermark
2. Pulls only new records from SQL Server
3. Loads new records into Snowflake RAW
4. Updates metadata timestamps

---

# Snowflake Warehouse

## Warehouse Layers

### RAW Layer

Stores ingested source-system data.

### STAGING Layer

Stores cleaned and transformed warehouse models.

### MARTS Layer

Stores analytics-ready dimensions and fact tables.

---

# dbt Integration

The project uses dbt to manage warehouse transformations.

## dbt Features Implemented

* Modular SQL models
* Dependency management
* Lineage tracking
* Documentation generation
* Automated testing
* Star schema modeling

## Warehouse Models

### Staging Models

* stg_customers
* stg_orders
* stg_products
* stg_order_items

### Dimension Models

* dim_customers
* dim_products

### Fact Models

* fact_sales

---

# Data Quality Testing

Automated dbt tests validate:

* unique primary keys
* non-null constraints
* referential integrity
* warehouse relationships

## Examples

* unique customer_id validation
* not_null email validation
* fact-to-dimension relationship checks

---

# Deduplication Strategy

The platform implements warehouse deduplication logic using:

```sql
ROW_NUMBER()
```

This ensures:

* latest records are retained
* duplicate incremental loads are handled safely
* warehouse models remain analytics-ready

---

# Apache Airflow Orchestration

Airflow orchestrates:

* dbt runs
* dbt tests
* pipeline scheduling
* operational execution flow

## Airflow DAGs

### dbt_transformation_pipeline

Runs:

1. dbt transformations
2. dbt tests

---

# Observability & Monitoring

The platform includes operational telemetry and audit logging.

## Pipeline Audit Logging

A Snowflake audit table tracks:

* pipeline executions
* success/failure states
* records processed
* execution duration
* error messages

---

# Failure Alerting

Airflow SMTP email alerting has been configured for:

* task failures
* DAG failures
* operational monitoring

The platform uses:

* Gmail SMTP
* Airflow email backend
* automated failure notifications

---

# Security & Configuration Management

The platform uses environment-driven configuration.

## Security Practices

* No hardcoded credentials
* `.env` configuration management
* `.gitignore` secret protection
* dbt environment variable injection
* centralized connection management

---

# Repository Structure

```text
retail-data-migration/
│
├── airflow/
│   ├── dags/
│   ├── logs/
│   └── plugins/
│
├── data/
│   └── raw/
│
├── docker/
│   └── Dockerfile.airflow
│
├── etl/
│   ├── extract/
│   └── db_connection.py
│
├── retail_dbt/
│   ├── models/
│   ├── target/
│   └── profiles.yml
│
├── snowflake/
│   └── snowflake_connection.py
│
├── .env
├── .gitignore
├── config.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Running the Project

## Start Infrastructure

```bash
docker compose up -d
```

---

## Run Incremental ETL

```bash
python -m etl.extract.incremental_extract
```

---

## Run dbt Models

```bash
cd retail_dbt

dbt run
```

---

## Run dbt Tests

```bash
cd retail_dbt

dbt test
```

---

## Generate dbt Documentation

```bash
cd retail_dbt

dbt docs generate

dbt docs serve --port 8081
```

---

# Future Enhancements

## Planned Improvements

* GitHub Actions CI/CD
* Slack alerting
* Terraform infrastructure provisioning
* Great Expectations integration
* Snowflake role-based access control
* Kafka streaming ingestion
* Power BI dashboards
* Containerized deployment improvements
* Infrastructure as Code

---

# Key Engineering Concepts Demonstrated

## Data Engineering

* ETL pipeline development
* Incremental ingestion
* Metadata-driven processing
* Warehouse loading

## Analytics Engineering

* dbt transformations
* Star schema modeling
* Lineage management
* Warehouse testing

## Platform Engineering

* Dockerized infrastructure
* Operational telemetry
* Failure alerting
* Orchestration
* Environment-based configuration

## DevOps Foundations

* Secret management
* CI/CD preparation
* Reproducible environments
* Dependency management

---

# Status

Project actively under development.

Current focus areas:

* CI/CD automation
* deployment workflows
* platform hardening
* operational maturity
