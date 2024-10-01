from config.dbconfig import pg_config
import psycopg2 as ps
class IncomingDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['database'],
                                                            pg_config['user'],
                                                            pg_config['password'],
                                                            pg_config['host'])
        self.conn = ps.connect(connection_url)

    def getAllIncoming(self):
        cursor = self.conn.cursor()
        result = []
        query = 'select incoming_id, trans_id, trans_qty, trans_part, trans_supplier from trans_incoming order by incoming_id'
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        self.conn.commit()
        self.conn.close()
        return result

    def searchById(self, pid):
        cursor = self.conn.cursor()
        query = 'select incoming_id, trans_id, trans_qty, trans_part, trans_supplier from trans_incoming where incoming_id=%s' 
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        return result
    
    def insertIncoming(self, id, data):
        cursor = self.conn.cursor()
        # Create query from request data
        query = f'''insert into trans_incoming(trans_id, trans_qty, trans_part, trans_supplier) 
        values({id}, '{data["TRANS_QTY"]}', '{data["TRANS_PART"]}', '{data["TRANS_SUPPLIER"]}') returning incoming_id'''
        # Try-Except block for error handling
        try:
            # Execute the query
            cursor.execute(query)
        # Error checking
        except ps.errors.UniqueViolation as uv:
            error = 'Database Error: Duplicate data received, check submission data.'
            return error, 400
        else:
            out = cursor.fetchone()[0]
            result = f'Incoming Transaction added with ID: {out}', data
            self.conn.commit()
            self.conn.close()
            return result
    
    def updateIncoming(self, id, data):
        cursor = self.conn.cursor()

        set_clause = ', '.join([f'{column} = %s' for column in data.keys()])
        # Create query from request data

        query = f'''UPDATE trans_incoming
                    SET {set_clause}
                    WHERE incoming_id = %s'''
        try:
            cursor.execute(query, tuple(data.values()) + (id,))

        # Error checking
        except ps.errors.UniqueViolation as uv:
            return 'Database Error: Duplicate data received, check submission data.'
        except ps.errors.ForeignKeyViolation as fk:
            return 'Database Error: Invalid part id or warehouse id specified'
        except ps.errors.CheckViolation as cv:
            return 'Database Error: Stock exceeds rack capacity'
        else:
            # Close connection to DB
            self.conn.commit()
            self.conn.close()
            result = data
            return result
    