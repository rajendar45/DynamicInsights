import cx_Oracle as oracle
import pandas as pd
oracle.init_oracle_client(lib_dir="/Users/AyapillaS/Oracle/instantclient_19_8", config_dir="/Users/AyapillaS/Oracle/instantclient_19_8")

def execute_query(query):
    
    # Connect to the Oracle database
    connection = oracle.connect("SRADMIN", "SRADMIN", "ece01d.ddscdl.es.ad.adp.com:1521/ece200d_svc1")

    # Create a cursor object to execute SQL statements
    cursor = connection.cursor()

    try:
        # Execute the query
        cursor.execute(query)

        # Fetch all the rows from the result set
        rows = cursor.fetchall()

        # Convert the rows into a pandas DataFrame
        results = pd.DataFrame(rows)

        # Set the column names based on the cursor description
        results.columns = [desc[0] for desc in cursor.description]

        return results
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()