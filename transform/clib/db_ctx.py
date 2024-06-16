"""
This library is to manage the Connection the RDS context
"""
import os
from psycopg2 import connect
from psycopg2.extensions import STATUS_READY
from typing import Optional, Tuple

def get_credentials() -> dict:
    """
    This method will get the OS credentials from environment
    
    :param: None
    
    :returns: (dict), with different credentials
    """
    return {
        "host"    : os.getenv("HOST"),
        "user"    : os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "database": os.getenv("DBNAME"),
        "port"    : os.getenv("PORT"),
    }

class SqlContext():
    """
    Class to connect to postgresql and perform sql operations
    
    :param host: (str), Ip address of the postgresql db
    :param user: (str), user name to use for postgresql connection
    :param password: (str), password of the username to use for postgresql connection
    :param database: (str), database name to connect
    :param port: (str), port to use for Ip address connection
    
    :returns: None
    """
    def __init__(self, host: str, user: str, password: str, database: str, port: str) -> None:
        
        if not isinstance(host, str):
            raise TypeError("host must be a string")
        if not isinstance(user, str):
            raise TypeError("user must be a string")
        if not isinstance(password, str):
            raise TypeError("password must be a string")
        if not isinstance(database, str):
            raise TypeError("database must be a string")
        if not isinstance(port, str):
            raise TypeError("port must be a string")
        
        self.cursor = None
        self.connection = connect(
            # Database connection parameters
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port,
        )
    
    def __enter__(self) -> None:
        """
        This module connects to a Db in the postgresql
        """
        # Check the connection status
        return self
    
    def __exit__(self, exc_type: any, exc_value: any, traceback: any) -> None:
        """
        This module is used to close the connection of the postgresql db
        
        :param exc_type: type of exception occurring
        :param exc_value: exception instance released
        :param traceback: exception traceback
        
        :return: None
        """
        if self.cursor:
            self.cursor.close()
        
        if self.connection:
            self.connection.commit()
            self.connection.close()
            
    def execute_query(
        self,
        query    : str,
        query_arg: Optional[dict] = None,
        fetch    : Optional[bool] = True,
        offset   : Optional[int] = None,
        limit    : Optional[int] = None,
    ) -> Tuple[int, dict]:
        """
        This method is used to execute any query and to protect the db from any sql injection
        
        :param query: (str), query string to execute
        :param fetch: (bool), used for selection queries. Default to True
        :param query_args: (dict), used to replace arguments in the query. Default to None
        :param offset: (int), if we want to use limit and offset with the cursor. Default to None
        :param limit: (int), if we want to use limit and offset with the cursor. Default to None
        
        :returns: Tuple(int, dict), the row count & the result. (None, None) if fetch is False.
        """
        if not isinstance(query, str):
            raise TypeError("query must be a string")
        if query_arg and not isinstance(query_arg, dict):
            raise TypeError("query_arg must be a dict")
        self.cursor = self.connection.cursor()
        # To prohibit sql injection
        self.cursor.execute(query, query_arg)
        
        if fetch:
            if not isinstance(fetch, bool):
                raise TypeError("fetch must be a boolean")
            count_rows = self.cursor.rowcount

            if offset:
                if not isinstance(offset, int):
                    raise TypeError("offset must be an integer")
                self.cursor.fetchmany(offset)

            if limit:
                if not isinstance(limit, int):
                    raise TypeError("limit must be an integer")
                results = self.cursor.fetchmany(limit)
            else:
                results = self.cursor.fetchall()
        
            return count_rows, results

        return None, None
    
    def check_connection(self) -> None:
        """
        To log connection to the postgreSQL db
        
        :param: None
        
        :returns: None
        """
        if self.connection.status == STATUS_READY:
            print("The connection is ready for use.")
        else:
            print("The connection is not ready.")