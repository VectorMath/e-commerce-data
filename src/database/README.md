# Module that contain work with databases

Here contains db-modules, who are responsible for:
  * Connection to databases
  * Working with a database by python code

## Structure

[**IClient**](IClient.py) - the interface of DB-Client, for every module have class realization.

[**IConnector**](IConnector.py) - the interface that responsible for connect to databases.

[**postgres**](postgres) - submodule that contain realization for work with databases of Postgres.