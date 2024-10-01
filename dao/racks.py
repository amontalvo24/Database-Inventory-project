from config.dbconfig import pg_config
import psycopg2 as ps

class RacksDAO:
    def __init__(self): 
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['database'],
                                                                pg_config['user'],
                                                                pg_config['password'],
                                                                pg_config['host'])
        self.conn = ps.connect(connection_url)

    def getAllRacks(self):
        cursor = self.conn.cursor()
        result = []
        query = 'select rack_id, rack_capacity, rack_stock, part_id, ware_id from racks order by rack_id'
        cursor.execute(query)
        for row in cursor:
             result.append(row)
        self.conn.commit()
        self.conn.close()
        return result

    def searchById(self, rid):
        cursor = self.conn.cursor()
        query = 'select rack_id, rack_capacity, rack_stock, part_id, ware_id from racks where rack_id=%s'
        cursor.execute(query, (rid,))
        result = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return result 
    
    def searchByWareAndPartId(self, wid, pid):
        cursor = self.conn.cursor()
        query = 'select rack_id, rack_capacity, rack_stock, part_id, ware_id from racks where ware_id=%s and part_id=%s'
        cursor.execute(query, (wid, pid))
        result = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return result
    
    def insertRack(self, data):
        cursor = self.conn.cursor()

        query = f'''insert into racks(RACK_CAPACITY, RACK_STOCK, PART_ID, WARE_ID)
        values('{data["RACK_CAPACITY"]}', '{data["RACK_STOCK"]}', '{data["PART_ID"]}', '{data["WARE_ID"]}') returning rack_id'''
            # Try-Except block for error handling
        try:
            # Execute the query
            cursor.execute(query)
        # Error checking
        except ps.errors.UniqueViolation as uv:
            return 'Database Error: Duplicate data received, check submission data.'
        except ps.errors.ForeignKeyViolation as fk:
            return 'Database Error: Invalid part id or warehouse id specified'
        except ps.errors.CheckViolation as cv:
            return 'Database Error: Stock exceeds rack capacity'
        else:
            out = cursor.fetchone()[0]
            result = f'New Rack added with ID: {out}', data
            # Close connection to DB
            self.conn.commit()
            self.conn.close()
            return result
        
    def updateRack(self, rid, data):

        cursor = self.conn.cursor()

        try:
            # Validate rack_id exists in the database
            validation_query = 'SELECT COUNT(*) FROM racks WHERE RACK_ID = %s'
            cursor.execute(validation_query, (rid,))
            if cursor.fetchone()[0] == 0:
                return f"Rack with ID:{rid} does not exist. Unable to update."

            # Check for at least one key-value pair
            if not data or not any(data.values()):
                return "Data Error: Insufficient or invalid data. Please provide at least one key-value pair."

            # Construct the SET clause for the update query
            set_clause = ', '.join([f'{column} = %s' for column in data.keys()])

            # Create the update query
            update_query = f'''UPDATE racks
                            SET {set_clause}
                            WHERE RACK_ID = %s'''
            
            # Execute the update query
            cursor.execute(update_query, tuple(data.values()) + (rid,))
            self.conn.commit()

            return f"Rack with ID {rid} has been successfully updated."

        except (ps.errors.UniqueViolation):
            return "Database Error: Duplicate data received, check submission data."
        except(ps.errors.ForeignKeyViolation):
            return "Database Error: Foreign key violation, check submission data."
        except(ps.errors.CheckViolation):
            return "Database Error: Exceeded rack capacity, check submission data."
        except ValueError as ve:
            return str(ve), 400
        except Exception as e:
            return f'Error updating rack with ID {rid}: {str(e)}'
        finally:
            # Close connection to DB
            self.conn.close()
    
    def deleteRack(self, rid):
        try:
            with self.conn.cursor() as cursor:
                # Validate rack_id given exists in warehouses table
                validation_query = 'SELECT COUNT(*) FROM racks WHERE RACK_ID = %s'
                cursor.execute(validation_query, (rid,))
                result = cursor.fetchone()

                if result[0] == 0:
                    # Rack ID does not exist
                    return f"Rack with ID:{rid} does not exist."

                # Delete the rack
                query_delete = 'DELETE FROM racks WHERE RACK_ID=%s'
                cursor.execute(query_delete, (rid,))
                self.conn.commit()
                return f"Rack with ID:{rid} has been successfully deleted."
        
        except Exception as e:
            return f"Error deleting rack with ID {rid}: {str(e)}"
        