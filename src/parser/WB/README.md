# WB Parser

The module that realize parsing-functional for web-store
[WildBerries](https://www.wildberries.ru/)

## Description of Python files

* [**AsyncRequesterWB**](AsyncRequesterWB.py) - class that extract API URLs of personal info and price history of
  product


* [**constants**](constants.py) - file with constant values that using in module


* [**ParserDictWB**](ParserDictWB.py) - class that extract info from dictionary. Using in class [ParserWB](ParserWB.py)


* [**ParserWB**](ParserWB.py) - realization of interface [IParser](../IParser.py) for web store Wildberries


* [**primary_data_script**](primary_data_script.py) - script that launching to collect primary data from web store 
  Wildberries. after finish give you 4 csv files, that will be contained in folder [csv](csv). For more detail look in
  comments of that script.

## Description of TXT files

* [**primary_data_run_output**](primary_data_run_output.txt) - txt file that contain output information of result
  from [primary_data_script](primary_data_script.py).
  Below is some information from file:

````
-----Chunk №17-----
Starting create table of json URLs
Finished - 88.94 seconds

[10 THREADS] Starting collect personal info about products
Finished - 56.31 seconds

[10 THREADS] Starting collect price history
Finished - 59.03 seconds

[10 THREADS] Starting collect feedbacks
Finished - 382.76 seconds
````

## Description of folders

* [**csv**](csv) - folder that contains result of [**primary_data_script**](primary_data_script.py) in csv-files. Here
  is information about files:
    * ### Feedback
      Contains info about feedbacks for products:
        * **Count rows:** ~9 000 000
        * **File size:** 0.98 GB
        * **Table structure:**

          |           root_id           |    product_id     |             date              |     comment     |       grade       |
          |:---------------------------:|:-----------------:|:-----------------------------:|:---------------:|:-----------------:|
          | the ID of section a product | The ID of product | Date when comment was created | Text of comment | Grade from 1 to 5 |

    * ### Price history
      Contains info about price history of products:
        * **Count rows:** ~118 000
        * **File size:** 3.25 MB
        * **Table structure:**

          |    product_id     |     date      |         price         |
          |:-----------------:|:-------------:|:---------------------:|
          | The ID of product | Date of price | Price on current date |
 
    * ### Products
      Contains personal info about products:
        * **Count rows:** 1 000
        * **File size:** 3.31 MB
        * **Table structure:**

          |           root_id           |    product_id     |             date             |       product_name       |      description       |              subj_name               |             subj_root_name              |      brand_name       |      size_table      |           min_size           |           max_size           |          color          |            made_in             |      compositions       |
          |:---------------------------:|:-----------------:|:----------------------------:|:------------------------:|:----------------------:|:------------------------------------:|:---------------------------------------:|:---------------------:|:--------------------:|:----------------------------:|:----------------------------:|:-----------------------:|:------------------------------:|:-----------------------:|
          | the ID of section a product | The ID of product | Date when product was parsed | Name of product on store | Description of product | The type of product (example: Cloth) | The subtype of product (example: Pants) | Name of product brand | All sizes of product | Minimal size from size table | Maximum size from size_table | Color that have product | Country where product was made | Compositions of product |

    * ### Urls
      Contains URLs of JSONs for tables **Products** and **Price history**:
        * **Count rows:** 1 000
        * **File size:** 165 KB
        * **Table structure:**

          |    product_id     |                      card_json_url                       |                          price_history_json_url                           |
          |:-----------------:|:--------------------------------------------------------:|:-------------------------------------------------------------------------:|
          | The ID of product | The URL where contains JSON that have info about product | The URL where contains JSON that have info about price history of product |