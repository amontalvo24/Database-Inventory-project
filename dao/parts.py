from config.dbconfig import pg_config
import psycopg2 as ps
class PartDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['database'],
                                                            pg_config['user'],
                                                            pg_config['password'],
                                                            pg_config['host'])
        self.conn = ps.connect(connection_url)

    def getAllParts(self):
        cursor = self.conn.cursor()
        result = []
        query = 'select part_id, part_name, part_price, part_type from parts order by part_id'
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        self.conn.commit()
        self.conn.close()
        return result

    def searchById(self, pid):
        cursor = self.conn.cursor()
        query = 'select part_id, part_name, part_price, part_type from parts where part_id=%s' 
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return result
    
    def insertPart(self,data):
        cursor = self.conn.cursor()
        # Create query from request data
        query = f'''insert into parts(PART_NAME, PART_PRICE, PART_TYPE) 
        values('{data["PART_NAME"]}', '{data["PART_PRICE"]}', '{data["PART_TYPE"]}') returning part_id'''
        # Try-Except block for error handling
        try:
            # Execute the query
            cursor.execute(query)
        # Error checking
        except ps.errors.UniqueViolation as uv:
            return 'Database Error: Duplicate data received, check submission data.'
        else:
            out = cursor.fetchone()[0]
            result = f'New Part added with ID: {out}', data
            # Close connection to DB
            self.conn.commit()
            self.conn.close()
            return result
        
    def updatePart(self, pid, data):
        cursor = self.conn.cursor()

        # Validate part_id given exists in parts table
        validation_query = 'SELECT COUNT(*) FROM parts WHERE PART_ID = %s'
        cursor.execute(validation_query, (pid,))
        result = cursor.fetchone()
        if result[0] == 0:
            # Part ID does not exist, handle the validation failure (raise an exception or return an error)
            return f"Part with ID {pid} does not exist."
    
        set_clause = ', '.join([f'{column} = %s' for column in data.keys()])
        # Create query from request data
        query = f'''UPDATE parts
                    SET {set_clause}
                    WHERE PART_ID = %s'''
        # Error handling
        try:
            cursor.execute(query, tuple(data.values()) + (pid,))
        except ps.errors.UniqueViolation as uv:
            return 'Database Error: Duplicate data received, check submission data.'
        
        else:
            # Close connection to DB
            self.conn.commit()
            self.conn.close()
            result = data
            return result
        
    def deletePart(self, pid):
        cursor = self.conn.cursor()

        #Validate part_id given exists in supplies table
        validation_query = 'SELECT COUNT(*) FROM parts WHERE PART_ID = %s'
        cursor.execute(validation_query, (pid,))
        result = cursor.fetchone()

        if result[0] == 0:
            # Part ID does not exist, handle the validation failure (raise an exception or return an error)
            return f"Part with ID:{pid} does not exist."
        
        query = 'delete from parts where part_id=%s'
        cursor.execute(query, (pid,))
        self.conn.commit()
        self.conn.close()
        return result
