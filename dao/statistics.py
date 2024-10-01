from flask import jsonify
from config.dbconfig import pg_config
import psycopg2 as ps

class StatisticsDAO():
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['database'],
                                                            pg_config['user'],
                                                            pg_config['password'],
                                                            pg_config['host'])
        self.conn = ps.connect(connection_url)

    def calculate_profit_by_year(self, wid):
        cur1 = self.conn.cursor()
        query = f'''SELECT EXTRACT(YEAR FROM trans_date) as year,
                      SUM(CASE WHEN trans_type = 'INCOMING' THEN (rack_stock * part_price)
                               WHEN trans_type = 'OUTGOING' THEN -(rack_stock * part_price)
                          ELSE 0 END) as profit
                FROM transactions
                JOIN racks ON transactions.rack_id = racks.rack_id
                JOIN parts ON racks.part_id = parts.part_id
                WHERE transactions.ware_id = {wid}
                GROUP BY year
                ORDER BY year'''

        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n = []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def get_top_5_racks_under_threshold(self, wid):
        cur1 = self.conn.cursor()
        query = f'''select *, (CAST(rack_stock AS DECIMAL)/rack_capacity) as capacity_threshold
                from racks
                where ware_id = {wid}
                group by rack_id, rack_capacity, rack_stock, part_id, ware_id
                having (CAST(rack_stock AS DECIMAL)/rack_capacity) < 0.25
                order by (CAST(rack_stock AS DECIMAL)/rack_capacity) ASC
                LIMIT 5;'''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n= []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def top_5_expensive_racks(self, wid):
        cur1 = self.conn.cursor()
        query = f'''SELECT racks.*, (parts.part_price*racks.rack_stock) as rack_value 
                    FROM racks
                    JOIN parts ON racks.part_id = parts.part_id WHERE racks.ware_id = {wid}
                    GROUP BY racks.rack_id, racks.rack_capacity, racks.rack_stock, racks.part_id, racks.ware_id, parts.part_price
                    ORDER BY (parts.part_price*racks.rack_stock) DESC
                    LIMIT 5'''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n= []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def get_top_3_supplier_trans(self, wid):
        cur1 = self.conn.cursor()
        query = f'''SELECT trans_supplier as supplier_id, count(*) as trans_count 
                    FROM trans_incoming NATURAL JOIN transactions where ware_id ={wid}
                    group by trans_supplier 
                    order by count(*) desc 
                    limit 3'''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n= []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def get_bottom_3_parts_type(self, wid):
        cur1 = self.conn.cursor()
        result = []
        query = f'''select part_type, SUM(rack_stock) as total_stock
                    from parts natural join racks
                    where ware_id = {wid}
                    group by 1
                    order by total_stock
                    LIMIT 3;'''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n= []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def get_bottom_3_days_smallest_incoming_price(self, wid):
        cur1 = self.conn.cursor()
        query = f'''select trans_date, sum(part_price * trans_qty) as trans_cost
                    from transactions natural inner join trans_incoming natural inner join parts
                    where ware_id = {wid} 
                    group by trans_date
                    order by trans_cost 
                    LIMIT 3;
                '''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n= []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def get_top_3_users_most_exchanges(self, wid):
        cur1 = self.conn.cursor()
        query = f'''select user_id, count(*) as receipt_amount
                from transactions
                where ware_id = {wid}
                and trans_type = 'EXCHANGE'
                group by user_id
                order by receipt_amount DESC
                limit 3;'''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n= []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data
    
    # Global Statistics DAO

    def get_top_10_warehouses_most_racks(self):
        cur1 = self.conn.cursor()
        result = []
        query = f'''SELECT ware_id, count(*) as rack_count 
                    FROM racks 
                    GROUP BY ware_id
                    ORDER BY count(*) DESC 
                    LIMIT 10;'''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n= []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def get_top_5_warehouses_most_incoming_trans(self):
        cur1 = self.conn.cursor()
        result = []
        query = f'''SELECT ware_id, count(*) as inc_transaction_count 
                    FROM transactions WHERE trans_type = 'INCOMING' 
                    GROUP BY 1 
                    ORDER BY count(*) DESC 
                    LIMIT 5;'''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n= []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def get_top_5_warehouses_most_deliveries_exchanges(self):
        cur1 = self.conn.cursor()
        result = []
        query = f'''SELECT trans_ware_supplier as ware_id, count(*) as delivered_exchanges 
                    FROM trans_exchange 
                    GROUP BY 1 
                    ORDER BY count(*) DESC 
                    LIMIT 5;'''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n= []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def get_top_3_users_most_trans(self):
        cur1 = self.conn.cursor()
        result = []
        query = f'''SELECT user_id, COUNT(*) as trans_count 
                    FROM transactions 
                    GROUP BY user_id 
                    ORDER BY count(*) DESC 
                    LIMIT 3;'''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n= []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def get_top_3_warehouses_least_outgoing_trans(self):
        cur1 = self.conn.cursor()
        result = []
        query = f'''SELECT ware_id, count(*) as outgoing_trans_count 
                    FROM transactions 
                    WHERE trans_type = 'OUTGOING' 
                    GROUP BY 1 
                    ORDER BY count(*) ASC 
                    LIMIT 3;'''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n= []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def get_top_3_warehouses_cities_most_trans(self):
        cur1 = self.conn.cursor()
        result = []
        query = f'''SELECT ware_city as city, count(*) as city_trans_count 
                    FROM transactions NATURAL JOIN warehouses 
                    GROUP BY city 
                    ORDER BY count(*) DESC 
                    LIMIT 3;'''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n= []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def parts_supplied_by_supplier(self, sid):
        cur1 = self.conn.cursor()
        result = []
        query = f'''SELECT parts.*, supplies.stock
                    FROM parts
                    JOIN supplies ON parts.part_id = supplies.part_id
                    WHERE supplies.supplier_id = {sid};
                    '''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n= []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def transactions_by_ware(self, uid):
        cur1 = self.conn.cursor()
        result = []
        query = f'''SELECT trans_id, trans_type, trans_date, ware_id, rack_id
                    FROM transactions
                    WHERE user_id = {uid}
                    group by ware_id, trans_id, trans_type, trans_date, user_id, rack_id;'''

        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n = []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

    def parts_in_ware(self, wid):
        cur1 = self.conn.cursor()
        result = []
        query = f'''SELECT parts.*
                    FROM parts
                    JOIN racks ON parts.PART_ID = racks.PART_ID
                    JOIN warehouses ON racks.WARE_ID = warehouses.WARE_ID
                    WHERE warehouses.WARE_ID = {wid}'''
        cur1.execute(query)
        result = cur1.fetchall()
        data = []
        col_n = []
        for desc in cur1.description:
            col_n.append(desc[0])
        for row in result:
            data.append(dict(zip(col_n, row)))
        self.conn.commit()
        self.conn.close()
        return data

