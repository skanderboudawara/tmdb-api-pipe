"""
This method is used to loop through sql files and init the DB
"""
import os
from .db_ctx import SqlContext, get_credentials

def run_sql_files(sql_folder_path: str) -> None:
    """
    This method will go through all the stored SQL file and commit them to PostgreSQL
    
    :param sql_folder_path: (str), path to the SQL files
    
    :return: None
    """
    if not isinstance(sql_folder_path, str):
        raise TypeError("sql_folder_path must be a string")
    # Define the order of subfolder
    subfolder_order = ['tables', 'functions', 'procedures', 'views']

    # Iterate over the subfolder in the specified order
    for subfolder in subfolder_order:
        subfolder_path = os.path.join(sql_folder_path, subfolder)
        if os.path.isdir(subfolder_path):
            sql_files = [f for f in os.listdir(subfolder_path) if f.endswith('.sql')]
            # Iterate over SQL files in the subfolder
            for sql_file in sql_files:
                print(f"processing {sql_file}")
                # Read the SQL file content
                with open(os.path.join(subfolder_path, sql_file), 'r') as f:
                    sql_query = f.read()
                    with SqlContext(**get_credentials()) as sql_context:
                        sql_context.execute_query(sql_query, fetch=False)

# Run the app
if __name__ == '__main__':
    run_sql_files("/app/sql")
