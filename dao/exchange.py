from config.dbconfig import pg_config
import psycopg2 as ps
class ExchangeDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['database'],
                                                            pg_config['user'],
                                                            pg_config['password'],
                                                            pg_config['host'])
        self.conn = ps.connect(connection_url)

    def getAllExchange(self):
        cursor = self.conn.cursor()
        result = []
        query = 'select exchange_id, trans_id, trans_qty, trans_part, trans_ware_supplier, supplier_user_id from trans_exchange order by exchange_id'
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        self.conn.commit()
        self.conn.close()
        return result

    def searchById(self, id):
        cursor = self.conn.cursor()
        query = 'select exchange_id, trans_id, trans_qty, trans_part, trans_ware_supplier, supplier_user_id from trans_exchange where exchange_id=%s' 
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return result
    
    def insertExchange(self, id, data):
        cursor = self.conn.cursor()
        # Create query from request data
        query = f'''insert into trans_exchange(trans_id, trans_qty, trans_part, trans_ware_supplier, supplier_user_id) 
        values('{id}', '{data["TRANS_QTY"]}', '{data["TRANS_PART"]}', '{data["TRANS_WARE_SUPPLIER"]}', '{data["SUPPLIER_USER_ID"]}') returning exchange_id'''
        # Try-Except block for error handling
        try:
            # Execute the query
            cursor.execute(query)
        # Error checking
        except ps.errors.UniqueViolation as uv:
            return 'Database Error: Duplicate data received, check submission data.'
        else:
            out = cursor.fetchone()[0]
            result = f'Exchange Transaction added with ID: {out}',data
            self.conn.commit()
            self.conn.close()
            return result
    
    def updateExchange(self, id, data):
        cursor = self.conn.cursor()
        query = '''update trans_exchange 
                set trans_id=%s, trans_qty=%s, trans_part=%s, trans_ware_supplier=%s, supplier_user_id=%s
                where trans_id=%s'''
        cursor.execute(query, (data[0], data[1], data[2], data[3], data[4], id))
        result = data
        self.conn.commit()
        self.conn.close()
        return result
    