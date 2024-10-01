from config.dbconfig import pg_config
import psycopg2 as ps

class WarehousesDAO:
    def __init__(self): 
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['database'],
                                                                pg_config['user'],
                                                                pg_config['password'],
                                                                pg_config['host'])
        self.conn = ps.connect(connection_url)

    def getAllWarehouses(self):
        cursor = self.conn.cursor()
        result = []
        query = 'select ware_id, ware_name, ware_budget, ware_street, ware_city, ware_country, ware_zipcode from warehouses order by ware_id'
        cursor.execute(query)
        for row in cursor:
             result.append(row)
        self.conn.commit()
        self.conn.close()
        return result
        
    def searchById(self, wid):
        cursor = self.conn.cursor()
        query = 'select ware_id, ware_name, ware_budget, ware_street, ware_city, ware_country, ware_zipcode from warehouses where ware_id=%s'
        cursor.execute(query, (wid,))
        result = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return result
    
    def insertWarehouse(self, data):
        cursor = self.conn.cursor()
        # Create query from request data
        query = f'''insert into warehouses(WARE_NAME, WARE_STREET, WARE_CITY, WARE_COUNTRY, WARE_ZIPCODE, WARE_BUDGET) 
        values('{data["WARE_NAME"]}', '{data["WARE_STREET"]}', '{data["WARE_CITY"]}', '{data["WARE_COUNTRY"]}', '{data["WARE_ZIPCODE"]}', '{data["WARE_BUDGET"]}') returning ware_id'''
        # Try-Except block for error handling
        try:
            # Execute the query
            cursor.execute(query)
        # Error checking
        except ps.errors.UniqueViolation as uv:
            return f'Database Error: Duplicate data received, check submission data.'
        else:
            out = cursor.fetchone()[0]
            result = f'New Warehouse added with ID: {out}', data
            self.conn.commit()
            self.conn.close()
            result = data
            return result
        
    def updateWarehouse(self, wid, data):
        cursor = self.conn.cursor()

        # Validate ware_id given exists in warehouses table
        validation_query = 'SELECT COUNT(*) FROM warehouses WHERE WARE_ID = %s'
        cursor.execute(validation_query, (wid,))
        result = cursor.fetchone()
        if result[0] == 0:
            # Warehouse ID does not exist, handle the validation failure (raise an exception or return an error)
            return f"Warehouse with ID {wid} does not exist."
    
        set_clause = ', '.join([f'{column} = %s' for column in data.keys()])
        # Create query from request data
        query = f'''UPDATE warehouses
                    SET {set_clause}
                    WHERE WARE_ID = %s'''
    
        cursor.execute(query, tuple(data.values()) + (wid,))
        
        # Error handling
        try:
            cursor.execute(query, tuple(data.values()) + (wid,))
        except ps.errors.UniqueViolation as uv:
            return 'Database Error: Duplicate data received, check submission data.'
        
        else:
            # Close connection to DB
            self.conn.commit()
            self.conn.close()
            result = data
            return result
    
    def deleteWarehouse(self, wid):
        cursor = self.conn.cursor()

        #Validate ware_id given exists in warehouses table
        validation_query = 'SELECT COUNT(*) FROM warehouses WHERE WARE_ID = %s'
        cursor.execute(validation_query, (wid,))
        result = cursor.fetchone()
        if result[0] == 0:
            # Warehouse ID does not exist, handle the validation failure (raise an exception or return an error)
            return f"Warehouse with ID {wid} does not exist."
        
        query = 'delete from warehouses where ware_id=%s'
        cursor.execute(query, (wid,))
        self.conn.commit()
        self.conn.close()
        return result