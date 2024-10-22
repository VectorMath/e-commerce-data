<p align="center">
  <img src=docs/pictures/main.png alt="Main_picture">
</p>

# Contents

- ### [**Description of project**](#description-of-project)
- ### [**Main technology stack**](#main-technology-stack)
- ### [**Tables in Database**](#tables-in-database)
- ### [**Project structure**](#project-structure)

## Description of project

This project created for work with different **russian** web stores. In project, you can see:

 * **Data collection from internet source**


 * **Work with DB PostgreSQL**


 * **ETL/ELT operations with Apache AirFlow:**
   * **Updating data of existing products**
   * **Adding new products**
   * **Removing data of products that's doesn't exist already**
   * **Creating tables**

## Main technology stack

<p align="center">
  <img src=docs/pictures/main_tech_stack.png alt="main_tech_stack">
</p>

## Tables in Database

* ### Product
  Main table that contain personal information of products 
  
  |           root_id           |    product_id     |             date             |       product_name       |      description       |              subj_name               |             subj_root_name              |      brand_name       |      size_table      |           min_size           |           max_size           |          color          |            made_in             |      compositions       |
  |:---------------------------:|:-----------------:|:----------------------------:|:------------------------:|:----------------------:|:------------------------------------:|:---------------------------------------:|:---------------------:|:--------------------:|:----------------------------:|:----------------------------:|:-----------------------:|:------------------------------:|:-----------------------:|
  | the ID of section a product | The ID of product | Date when product was parsed | Name of product on store | Description of product | The type of product (example: Cloth) | The subtype of product (example: Pants) | Name of product brand | All sizes of product | Minimal size from size table | Maximum size from size_table | Color that have product | Country where product was made | Compositions of product |


* ### Price history
  Table that contain history of prices for products

  |    product_id     |     date      |         price         |
  |:-----------------:|:-------------:|:---------------------:|
  | The ID of product | Date of price | Price on current date |

* ### Price
  Table with actual prices on products. Created every week from table Price history

  |    product_id     |    price     |
  |:-----------------:|:------------:|
  | The ID of product | Actual price |

* ### Feedbacks
  Table that contain users feedbacks for products

  |           root_id           |    product_id     |             date              |     comment     |       grade       |
  |:---------------------------:|:-----------------:|:-----------------------------:|:---------------:|:-----------------:|
  | the ID of section a product | The ID of product | Date when comment was created | Text of comment | Grade from 1 to 5 |

* ### Grade
  Table that contain actual grade for products. Created every week from table Feedbacks

  |    product_id     |                    mean_grade                     |                    mean_grade_filtered                     |          median_grade           |          median_grade_filtered           |          mode_grade           |          mode_grade_filtered           |
  |:-----------------:|:-------------------------------------------------:|:----------------------------------------------------------:|:-------------------------------:|:----------------------------------------:|:-----------------------------:|:--------------------------------------:|
  | The ID of product | Average product grade based on arithmetic average | Filtered average product grade based on arithmetic average | Average product grade by median | Filtered average product grade by median | Average product grade by mode | Filtered average product grade by mode |


## Project structure

 * [**src**](src) - The folder with main code part of project.
   * [**parser**](src/parser) - The folder that contains functional with parsing different web store.


 * [**docs**](docs) - folder with resources for README documents.


 * [**tests**](tests) - The folder with unit tests for functional in [**src**](src) folder.