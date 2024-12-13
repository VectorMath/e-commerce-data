<p align="center">
  <img src=docs/pictures/main.png alt="Main_picture">
</p>

# Contents

- ### [**Description of project**](#description-of-project)
- ### [**Main technology stack**](#main-technology-stack)
- ### [**Data model**](#data-model)
- ### [**Tables in Database**](#tables-in-database)
- ### [**DAG Dependencies**](#dag-dependencies)
- ### [**Project structure**](#project-structure)

## Description of project

This project created for work with different **russian** web stores. In project, you can see:

* **Data collection from internet source**


* **Work with DB PostgreSQL**


* **ETL/ELT operations with Apache AirFlow:**
    * **Updating data of existing products**
    * **Adding new products**
    * **Removing data of products that's does not exist already**
    * **Creating tables**

## Main technology stack

<p align="center">
  <img src=docs/pictures/main_tech_stack.png alt="main_tech_stack">
</p>

## Data model

<p align="center">
  <img src=docs/pictures/data_model.png alt="data_model">
</p>

## Tables in Database

* ### Products
  Main table that contain personal information of products

  |           root_id           |    product_id     |             date             |       product_name       |      description       |              subj_name               |             subj_root_name              |      brand_name       |      size_table      |           min_size           |           max_size           |          color          |            made_in             |      compositions       |
    |:---------------------------:|:-----------------:|:----------------------------:|:------------------------:|:----------------------:|:------------------------------------:|:---------------------------------------:|:---------------------:|:--------------------:|:----------------------------:|:----------------------------:|:-----------------------:|:------------------------------:|:-----------------------:|
  | the ID of section a product | The ID of product | Date when product was parsed | Name of product on store | Description of product | The type of product (example: Cloth) | The subtype of product (example: Pants) | Name of product brand | All sizes of product | Minimal size from size table | Maximum size from size_table | Color that have product | Country where product was made | Compositions of product |

* ### URLs
  Table that contain URLs of information in JSON-format

  |    product_id     |         card_json_url          |     price_history_json_url     |
    |:-----------------:|:------------------------------:|:------------------------------:|
  | The ID of product | URL with product personal info | URL with product price history |

* ### Price history
  Table that contain history of prices for products

  |    product_id     |     date      |         price         |
    |:-----------------:|:-------------:|:---------------------:|
  | The ID of product | Date of price | Price on current date |

* ### Price
  Table with actual prices on products. Created every day from table Price history

  |    product_id     |    price     |
    |:-----------------:|:------------:|
  | The ID of product | Actual price |

* ### Feedbacks
  Table that contain users feedbacks for products

  |           root_id           |    product_id     |             date              |     comment     |       grade       |
    |:---------------------------:|:-----------------:|:-----------------------------:|:---------------:|:-----------------:|
  | the ID of section a product | The ID of product | Date when comment was created | Text of comment | Grade from 1 to 5 |

* ### Grade
  Table that contain actual grade for products. Created every day from table Feedbacks

  |    product_id     |                    mean_grade                     |                    mean_grade_filtered                     |          median_grade           |          median_grade_filtered           |          mode_grade           |          mode_grade_filtered           |
    |:-----------------:|:-------------------------------------------------:|:----------------------------------------------------------:|:-------------------------------:|:----------------------------------------:|:-----------------------------:|:--------------------------------------:|
  | The ID of product | Average product grade based on arithmetic average | Filtered average product grade based on arithmetic average | Average product grade by median | Filtered average product grade by median | Average product grade by mode | Filtered average product grade by mode |

* ### Grade history
  Table that contain actual grade for products. Created every day from table, taking data from table **Grade**.

  |    product_id     |                    mean_grade                     |                    mean_grade_filtered                     |          median_grade           |          median_grade_filtered           |          mode_grade           |          mode_grade_filtered           |
    |:-----------------:|:-------------------------------------------------:|:----------------------------------------------------------:|:-------------------------------:|:----------------------------------------:|:-----------------------------:|:--------------------------------------:|
  | The ID of product | Average product grade based on arithmetic average | Filtered average product grade based on arithmetic average | Average product grade by median | Filtered average product grade by median | Average product grade by mode | Filtered average product grade by mode |

## DAG Dependencies

<p align="center">
  <img src=docs/pictures/dag_depends.png alt="dag_depends">
</p>

## Project structure

* [**dags**](dags) - The folder with Airflow DAGs.
    * [**add**](dags/add) - The folder with DAGs that make functional of adding new data in database.
    * [**create**](dags/create) The folder with DAGs that make functional of creating tables in database.
    * [**remove**](dags/remove) - The folder with DAGs that make functional of removing data of products from all tables
      in database.
    * [**update**](dags/update) - The folder with DAGs that make functional of updating information the existing
      products in database.


* [**docs**](docs) - folder with resources for README documents.


* [**dumps**](dumps) - folder with database back-up.


* [**src**](src) - The folder with main code part of project.
    * [**parser**](src/parser) - The folder that contains functional with parsing different web store.
    * [**database**](src/database) - The folder that contains functional with different databases.


* [**tests**](tests) - The folder with unit tests for functional in [**src**](src) folder.
    * [**parser**](tests/parser) - unit-tests for module **parser**.
    * [**database**](tests/database) - unit-tests for module **database**.


* [**docker-compose**](docker-compose.yaml) - Main Docker Compose file, that up container with DB and Airflow.


* [**Dockerfile**](Dockerfile) - Dockerfile that make image of DB with init-file from foler [**dumps**](dumps).


* [**Dockerfile-airflow-playwright**](Dockerfile-airflow-playwright) - Dockerfile that make image of Airflow and install
  library playwright for async code.