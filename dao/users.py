from config.dbconfig import pg_config
import psycopg2 as ps


class UserDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['database'],
                                                                    pg_config['user'],
                                                                    pg_config['password'],
                                                                    pg_config['host'])
        self.conn = ps.connect(connection_url)

    def getAllUsers(self):
        cursor = self.conn.cursor()
        result = []
        query = "select user_id, user_name, user_lname, user_email, user_pass, ware_id from users order by user_id asc"
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        self.conn.commit()
        self.conn.close()
        return result

    def searchById(self, uid):
        cursor = self.conn.cursor()
        query = "select user_id, user_name, user_lname, user_email, user_pass, ware_id from users where user_id=%s"
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        self.conn.commit()
        self.conn.close()
        return result

    def insertUser(self, data):
        cursor = self.conn.cursor()
        # Create query from request data
        ware_id_query = 'select count(*) from warehouses where ware_id = %s;'
        cursor.execute(ware_id_query, (data['WARE_ID'],))
        ware_id_exists = cursor.fetchone()[0] > 0
        if not ware_id_exists:
            return f'''Invalid ware_id: {data["WARE_ID"]}. This warehouse id does not exist in the database.'''

        query = f'''insert into users(USER_NAME, USER_LNAME, USER_EMAIL, USER_PASS, WARE_ID) 
        values('{data["USER_NAME"]}', '{data["USER_LNAME"]}', '{data["USER_EMAIL"]}', '{data["USER_PASS"]}', '{data["WARE_ID"]}') returning user_id'''
        # Try-Except block for error handling
        try:
            # Execute the query
            cursor.execute(query)
        # Error checking
        except ps.errors.UniqueViolation as uv:
            return f'Database Error: Duplicate data received, check submission data.'
        else:
            out = cursor.fetchone()[0]
            result = f'New User added with ID: {out}', data
            self.conn.commit()
            self.conn.close()
            return result

    def updateUser(self, uid, data):
        cursor = self.conn.cursor()

        # Validate user_id given exists in users table
        validation_query = 'SELECT COUNT(*) FROM USERS WHERE USER_ID = %s'
        cursor.execute(validation_query, (uid,))
        result = cursor.fetchone()
        if result[0] == 0:
            # User ID does not exist, handle the validation failure (raise an exception or return an error)
            return f"User with ID {uid} does not exist."

        set_clause = ', '.join([f'{column} = %s' for column in data.keys()])
        # Create query from request data
        query = f'''UPDATE USERS
                    SET {set_clause}
                    WHERE USER_ID = %s'''

        cursor.execute(query, tuple(data.values()) + (uid,))

        self.conn.commit()
        self.conn.close()
        return data

    def deleteUser(self, uid):
        cursor = self.conn.cursor()

        # Validate user_id given exists in users table
        validation_query = 'SELECT COUNT(*) FROM USERS WHERE USER_ID = %s'
        cursor.execute(validation_query, (uid,))
        result = cursor.fetchone()
        if result[0] == 0:
            # User ID does not exist, handle the validation failure (raise an exception or return an error)
            return f"User with ID {uid} does not exist."

        query = 'DELETE from USERS where USER_ID=%s'
        cursor.execute(query, (uid,))
        self.conn.commit()
        self.conn.close()
        return result
