# Important
Configure the .env file

PS: some data are shown in the readme file for exercise purpose. Else credential must not be exposed.
```
BEARER_TOKEN=<Add the TMDB Token Here>
DBNAME=soyhuce_db  # These are configured in the Docker image
USER=postgres  # These are configured in the Docker image
PASSWORD=soyhuce  # These are configured in the Docker image
HOST=192.168.92.22  # These are configured in the Docker image
PORT=5432  # These are configured in the Docker image
```

# Installation & Running Steps:

1. Run `docker-compose build`.
2. Execute `docker-compose up -d`.

# Docker Images:
- **PgAdmin4**: For accessing the PostgreSQL db.
- **PostgreSQL 14.8**: Selected based on the latest version available.
- **Python 3.10**: Slim version.

# Setting Up:

Once the Docker Compose process completes and the container images are up, you have two options:

1. From the Docker terminal of the Python image, execute `sh /app/menu.sh`.
2. Attach the image to Docker using VScode.

# Solution

## Goal:
The primary objective is to retrieve specific information about all released or planned movies and visualize it through two graphs:
- Total budget vs. revenue per year.
- Count of movies per year by genre.

## Code Architecture:
- **sql**: Contains SQL files to initialize the database with various tables, functions, procedures, and views.
- **clib** (Custom Library): Contains code to handle requests and populate the PostgreSQL database.
  - A `SQLContext` class ensures proper committing and closing of cursors.
- **dashboard**: Utilizes the `dash` library for visualization.
- **test**: Includes test examples using `pytest`.

## Process:

1. **MovieList Processing**: Populate the `movie_list` table with data from the `MovieList`.
   
2. **MovieInfo Retrieval**:
    - Utilize two options:
        1. **get_movie_array Function**: Returns the full list of `movie_id`s or those that have not been processed yet.
        2. **insert_or_update_info Procedure**: Updates existing rows or inserts new ones based on the `movie_id`.

3. **Movies Request Status View**: Use the `movies_request_status` view to identify all movies that have not been processed for investigation.

4. **Dashboard Views**:
    - Two views are created for dashboard purposes:
        1. **budget_revenue_per_year**: Presents the total budget vs. revenue per year.
        2. **movie_genre_yearly_count**: Displays the count of movies per year by genre.



# Critique & Next Steps:
- Enhance code coverage to achieve 100%.
- Use Logger instead of printing.
- Implement a scheduler solution for retrieving new data (options like Airflow or CronJob).
- Develop a more comprehensive dashboard.
