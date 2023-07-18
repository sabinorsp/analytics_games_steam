# analytics_games_steam:
This project is about process analytics, including ETL (Extract, Transform, Load) for a website Steam, exploratory data analysis, and dashboards configurations.

## etl_steam:
 ETL (Extract, Transform, Load) process to webscrape the Steam game list page and load it into a relational database, PostgreSQL, using Docker.

### How to Run: 
Configure Postegre server local with docker:  
1 - Install docker and docker-compose;  
2 - Create docker volume "dbsteam";  
3 - Run docker compose;  

Run etl_steam.py