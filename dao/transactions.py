from config.dbconfig import pg_config
import psycopg2 as ps
class TransactionsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['database'],
                                                            pg_config['user'],
                                                            pg_config['password'],
                                                            pg_config['host'])
        self.conn = ps.connect(connection_url)

    def getAllTransactions(self):
        cursor = self.conn.cursor()
        result = []
        query = 'select trans_id, trans_type, trans_date, user_id, ware_id, rack_id from transactions order by trans_id'
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        self.conn.commit()
        self.conn.close()
        return result

    def searchById(self, pid):
        cursor = self.conn.cursor()
        query = 'select trans_id, trans_type, trans_date, user_id, ware_id, rack_id from transactions where part_id=%s' 
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return result
    
    def insertTransaction(self,data) -> int:
        cursor = self.conn.cursor()
        # Create query from request data
        query = f'''insert into transactions(trans_type, user_id, ware_id, rack_id) 
        values('{data["TRANS_TYPE"]}', '{data["USER_ID"]}', '{data["WARE_ID"]}', '{data["RACK_ID"]}') returning trans_id'''
        # Try-Except block for error handling
        try:
            # Execute the query
            cursor.execute(query)
        # Error checking
        except ps.errors.UniqueViolation as uv:
            return 'Database Error: Duplicate data received, check submission data.'
        else:
            out = cursor.fetchone()[0]
            result = f'New Trabsaction added with ID: {out}', data
            self.conn.commit()
            self.conn.close()
            return out
        
    def updateTransaction(self, data):
        cursor = self.conn.cursor()
        query = '''update transactions 
                set trans_type=%s, trans_date=%s, user_id=%s, ware_id=%s, rack_id=%s
                where trans_id=%s
                returning trans_id'''
        cursor.execute(query, (data[0], data[1], data[2], data[3], data[4]))
        result = cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return result
    