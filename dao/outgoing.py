from config.dbconfig import pg_config
import psycopg2 as ps
class OutgoingDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['database'],
                                                            pg_config['user'],
                                                            pg_config['password'],
                                                            pg_config['host'])
        self.conn = ps.connect(connection_url)

    def getAllOutgoing(self):
        cursor = self.conn.cursor()
        result = []
        query = 'select outgoing_id, trans_id, trans_qty, trans_part, trans_recipient from trans_outgoing order by outgoing_id'
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        self.conn.commit()
        self.conn.close()
        return result

    def searchById(self, pid):
        cursor = self.conn.cursor()
        query = 'select outgoing_id, trans_id, trans_qty, trans_part, trans_recipient from trans_outgoing where outgoing_id=%s' 
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return result
    
    def insertOutgoing(self, id, data):
        cursor = self.conn.cursor()
        # Create query from request data
        query = f'''insert into trans_outgoing(trans_id, trans_qty, trans_part, trans_recipient) 
        values('{id}', '{data["TRANS_QTY"]}', '{data["TRANS_PART"]}', '{data["TRANS_RECIPIENT"]}') returning outgoing_id'''
        # Try-Except block for error handling
        try:
            # Execute the query
            cursor.execute(query)
        # Error checking
        except ps.errors.UniqueViolation as uv:
            return 'Database Error: Duplicate data received, check submission data.'
        else:
            out = cursor.fetchone()[0]
            result = f'Outgoing Transaction added with ID: {out}', data
            self.conn.commit()
            self.conn.close()
            return result
    
    def updateOutgoing(self, id, data):
        cursor = self.conn.cursor()
        query = '''update trans_outgoing 
                set trans_id=%s, trans_qty=%s, trans_part=%s, trans_recipient=%s
                where trans_id=%s'''
        cursor.execute(query, (data[0], data[1], data[2], data[3], id))
        result = data
        self.conn.commit()
        self.conn.close()
        return result
    