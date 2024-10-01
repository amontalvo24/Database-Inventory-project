from config.dbconfig import pg_config
import psycopg2 as ps

class SuppliesDAO:
    def __init__(self): 
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['database'],
                                                                pg_config['user'],
                                                                pg_config['password'],
                                                                pg_config['host'])
        self.conn = ps.connect(connection_url)

    def getAllSupplies(self):
        cursor = self.conn.cursor()
        result = []
        query = 'select * from supplies order by supplies_id'
        cursor.execute(query)
        for row in cursor:
             result.append(row)
        self.conn.commit()
        self.conn.close()
        return result
    
    def searchById(self, sid):
        cursor = self.conn.cursor()
        query = 'select * from supplies where supplies_id=%s'
        cursor.execute(query, (sid,))
        result = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return result
    
    def searchBySupplierId(self, suid):
        cursor = self.conn.cursor()
        query = 'select * from supplies where supplier_id=%s'
        cursor.execute(query, (suid,))
        result = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return result
    
    def searchBySupplierAndPartId(self, suid, pid):
        cursor = self.conn.cursor()
        query = 'select * from supplies where supplier_id=%s and part_id=%s'
        cursor.execute(query, (suid, pid))
        result = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return result
    
    def insertSupplies(self, data):
        cursor = self.conn.cursor()

        query = f'''insert into supplies(SUPPLIER_ID, PART_ID, STOCK)
        values('{data["SUPPLIER_ID"]}', '{data["PART_ID"]}', '{data["STOCK"]}') returning supplies_id'''

        # Try-Except block for error handling
        try:
            # Execute the query
            cursor.execute(query)
        # Error checking
        except ps.errors.UniqueViolation as uv:
            return 'Database Error: Duplicate data received, check submission data.'
        except ps.errors.ForeignKeyViolation as fk:
            return 'Database Error: Invalid supplier id or part id specified.'
        else:
            out = cursor.fetchone()[0]
            result = f'New Supplies record added with ID: {out}', data
            # Close connection to DB
            self.conn.commit()
            self.conn.close()
            return result
        
    def updateSupplies(self, sid, data):
        cursor = self.conn.cursor()

        set_clause = ', '.join([f'{column} = %s' for column in data.keys()])
        # Create query from request data

        query = f'''UPDATE supplies
                    SET {set_clause}
                    WHERE SUPPLIES_ID = %s'''
        try:
            cursor.execute(query, tuple(data.values()) + (sid,))

        # Error checking
        except ps.errors.UniqueViolation as uv:
            return 'Database Error: Duplicate data received, check submission data.'
        except ps.errors.ForeignKeyViolation as fk:
            return 'Database Error: Invalid supplier id or part id specified'

        else:
            # Close connection to DB
            self.conn.commit()
            self.conn.close()
            result = data
            return result
        
    def deleteSupplies(self, sid):
        cursor = self.conn.cursor()

        #Validate supplies_id given exists in supplies table
        validation_query = 'SELECT COUNT(*) FROM supplies WHERE SUPPLIES_ID = %s'
        cursor.execute(validation_query, (sid,))
        result = cursor.fetchone()

        if result[0] == 0:
            # Supply ID does not exist, handle the validation failure (raise an exception or return an error)
            return f"Supply with ID {sid} does not exist."
        
        query = 'delete from supplies where supplies_id=%s'
        cursor.execute(query, (sid,))
        self.conn.commit()
        self.conn.close()
        return result