from flask import jsonify
from dao import UserDAO

# Boilerplate Users Handler class, FUNCTIONS ARE NOT FULLY IMPLEMENTED
class UserHandler:

    # Mapping query output to dictionary to return to user
    def mapToDict(self, t):
        dict = {}
        dict['id'] = t[0]
        dict['name'] = t[1]
        dict['lname'] = t[2]
        dict['email'] = t[3]
        dict['password'] = t[4]
        dict['wareid'] = t[5]
        return dict

    # Handler function to get all users from database
    def getAllUsers(self):
        dao = UserDAO()
        db_tuples = dao.getAllUsers()
        result = []
        for e in db_tuples:
            result.append(self.mapToDict(e))
        return jsonify(result)

    # Handler function to get user with specific id from database
    def searchById(self, user_id):
        dao = UserDAO()
        result = dao.searchById(user_id)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify("Not Found"), 404

    # Handler to insert a new user into database
    def insertUser(self, data):
        if "USER_NAME" not in data or "USER_LNAME" not in data or "USER_EMAIL" not in data or "USER_PASS" not in data or "WARE_ID" not in data:
            return jsonify("Key Error: Insufficient or invalid data"), 400            
        if data["USER_NAME"] == None or type(data["USER_NAME"]) is not str or len(data["USER_NAME"]) > 50:
            return jsonify("Data Error: Insufficient or invalid data for USER_NAME"), 400
        elif data["USER_LNAME"] == None or type(data["USER_LNAME"]) is not str or len(data["USER_LNAME"]) > 50:
            return jsonify("Data Error: Insufficient or invalid data  for USER_LNAME"), 400
        elif data["USER_EMAIL"] == None or type(data["USER_EMAIL"]) is not str or len(data["USER_EMAIL"]) > 100:
            return jsonify("Data Error: Insufficient or invalid data for USER_EMAIL"), 400
        elif data["USER_PASS"] == None or type(data["USER_PASS"]) is not str or len(data["USER_PASS"]) > 50:
            return jsonify("Data Error: Insufficient or invalid data for USER_PASS"), 400
        elif data["WARE_ID"] == None or type(data["WARE_ID"]) is not int:
            return jsonify("Data Error: Insufficient or invalid data for WARE_ID"), 400
        
        dao = UserDAO()
        result = dao.insertUser(data)
        if result == 'Database Error: Duplicate data received, check submission data.':
            return jsonify(result)
        elif result == f'''Invalid ware_id: {data["WARE_ID"]}. This warehouse id does not exist in the database.''':
            return jsonify(result)
        elif result:
            return jsonify(result)
        else:
            return jsonify("Operation failed"), 405

    # Handler to update an existing user record in the database
    def updateUser(self, uid, data):
        # Check if at least one key-value pair is provided
        if not data:
            return jsonify("Data Error: Insufficient data. Please provide at least one key-value pair."), 400

        # If present validate USER_NAME 
        if "USER_NAME" in data:
            if data["USER_NAME"] == None or type(data["USER_NAME"]) is not str or len(data["USER_NAME"]) > 50:
                return jsonify("Data Error: Insufficient or invalid data for USER_NAME"), 400
        # If present validate USER_LNAME 
        if "USER_LNAME" in data:
            if data["USER_LNAME"] == None or type(data["USER_LNAME"]) is not str or len(data["USER_LNAME"]) > 50:
                return jsonify("Data Error: Insufficient or invalid data for USER_LNAME"), 400
        # If present validate USER_EMAIL 
        if "USER_EMAIL" in data:
            if data["USER_EMAIL"] == None or type(data["USER_EMAIL"]) is not str or len(data["USER_EMAIL"]) > 100:
                return jsonify("Data Error: Insufficient or invalid data for USER_EMAIL"), 400
        if "USER_PASS" in data:
            if data["USER_PASS"] == None or type(data["USER_PASS"]) is not str or len(data["USER_PASS"]) > 50:
                return jsonify("Data Error: Insufficient or invalid data for USER_PASS"), 400
        if "WARE_ID" in data:
            if data["WARE_ID"] == None or type(data["WARE_ID"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data for WARE_ID"), 400
        else:
            return jsonify("Key Error: Insufficient or invalid data"), 400
        
        dao = UserDAO()
        result = dao.updateUser(uid, data)

        if result == f"User with ID {uid} does not exist.":
            return jsonify(result)
        elif result:
            return jsonify(f"User {uid} has been updated.", result)
        else:
            return jsonify("Operation failed"), 405

    # Handler to delete an existing user from the database
    def deleteUser(self, uid):
        # Code needed
        dao = UserDAO()
        result = dao.deleteUser(uid)
        if result == f"User with ID {uid} does not exist.":
            return f"User with ID {uid} does not exist."
        elif result:
            return jsonify(f"User {uid} has been deleted.")
        else:
            return jsonify("Operation failed"), 405
