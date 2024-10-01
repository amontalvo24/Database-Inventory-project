from config.dbconfig import pg_config
import psycopg2 as ps

class SuppliersDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['database'],
                                                            pg_config['user'],
                                                            pg_config['password'],
                                                            pg_config['host'])
        self.conn = ps.connect(connection_url)

    def getAllSuppliers(self):
        cursor = self.conn.cursor()        
        result = []
        query = 'select * from suppliers order by supplier_id asc'
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        return result
    
    def searchById(self,supp_id):
        cursor = self.conn.cursor()
        query = 'select * from suppliers where supplier_id=%s order by supplier_id asc'
        cursor.execute(query, (supp_id,))
        result = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return result
    
    def insertSupplier(self, data):
        cursor = self.conn.cursor()
        result = []

        query = f'''insert into suppliers(SUPPLIER_NAME, SUPPLIER_STREET, SUPPLIER_CITY, SUPPLIER_COUNTRY, SUPPLIER_ZIPCODE)
        values('{data["SUPPLIER_NAME"]}', '{data["SUPPLIER_STREET"]}', '{data["SUPPLIER_CITY"]}', '{data["SUPPLIER_COUNTRY"]}', '{data["SUPPLIER_ZIPCODE"]}') returning supplier_id'''        
        # Try-Except block for error handling
        try:
            # Execute the query
            cursor.execute(query)
        # Error checking
        except ps.errors.UniqueViolation as uv:
            return 'Database Error: Duplicate data received, check submission data.'
        else:
            out = cursor.fetchone()[0]
            result = f'New Supplier added with ID: {out}', data
            # Close connection to DB
            self.conn.commit()
            self.conn.close()
            result = data
            return result

    def updateSupplier(self, data, supplier_id):
        cursor = self.conn.cursor()
        validation_query = 'SELECT COUNT(*) FROM suppliers WHERE SUPPLIER_ID = %s'
        cursor.execute(validation_query, (supplier_id,))
        result = cursor.fetchone()
        
        if result[0] == 0:
            return f"Supplier {supplier_id} does not exist!"
        
        set_clause = ', '.join([f'{column} = %s' for column in data.keys()])
        # Create query from request data
        query = f'''UPDATE suppliers
                    SET {set_clause}
                    WHERE SUPPLIER_ID = %s'''
        try:
            cursor.execute(query, tuple(data.values()) + (supplier_id,))

        # Error checking
        except ps.errors.UniqueViolation as uv:
            return 'Database Error: Duplicate data received, check submission data.'
        
        else:
            # Close connection to DB
            self.conn.commit()
            self.conn.close()
            result = data
            return result
        

       
    
    def deleteSupplier(self, supplier_id):
        cursor = self.conn.cursor()
        valid_query = 'SELECT COUNT(*) FROM suppliers WHERE supplier_id = %s'
        cursor.execute(valid_query, (supplier_id,))
        result = cursor.fetchone()
        if result[0] == 0:
            cursor.close()
            return f"Supplier {supplier_id} does not exist!"
        query = 'DELETE from SUPPLIERS where SUPPLIER_ID = %s'
        cursor.execute(query, (supplier_id,))
        self.conn.commit()
        self.conn.close()
        return result