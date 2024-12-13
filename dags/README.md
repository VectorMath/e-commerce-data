# ETL part of project

Folder **dags** contains ETL-code part of project, that work in Apache Airflow.

## DAG Dependencies

<p align="center">
  <img src=../docs/pictures/dag_depends.png alt="dag_depends">
</p>

## DAG Folders structure

In every folder with DAG has **3 python files:**

 * **X_Y_dag.py** - Python file with DAG and task init. That's main file for every DAG.


 * **X_Y_dag_config.py** - Python file with constant variables for DAG, like task IDs, SQL queries and more.


 * **X_Y_dag_task.py** - Python file with python callable functions for DAG tasks.

<p align="center">
  <img src=../docs/pictures/dag_files_depends.png alt="dag_files_depends">
</p>

## Folders

 * [**add**](add) - The folder with DAGs that make functional of adding new data in database.


 * [**create**](create) The folder with DAGs that make functional of creating tables in database.


 * [**remove**](remove) - The folder with DAGs that make functional of removing data of products from all tables
 in database.


 * [**update**](update) - The folder with DAGs that make functional of updating information the existing
 products in database.

## Python files
  * [**global_dag_config.py**](global_dag_config.py) - The python file with global common-constants for DAGs.


  * [**global_dag_task.py**](global_dag_task.py) - The python file with global common-tasks for DAGs.