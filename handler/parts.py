from flask import jsonify
from dao import PartDAO
class PartHandler:
    # Mapping query output to dictionary to return to user
    def mapToDict(self, t):
        dict = {}
        dict['id'] = t[0]
        dict['name'] = t[1]
        dict['price'] = t[2]
        dict['type'] = t[3]
        return dict
    
    # Handler function to get all parts from database
    def getAllParts(self):
        dao = PartDAO()
        db_tuples = dao.getAllParts()
        result = []
        for e in db_tuples:
            result.append(self.mapToDict(e))
        return jsonify(result)
    
    # Handler function to get part with specific id from database
    def searchById(self, pid):
        dao = PartDAO()
        result = dao.searchById(pid)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify("Not Found"), 404
        
    # Handler to insert a new part into database
    def insertPart(self, data):

        if "PART_NAME" not in data or "PART_PRICE" not in data or "PART_TYPE" not in data:
            return jsonify("Key Error: Insufficient or invalid data"), 400            
        if data["PART_NAME"] == None or type(data["PART_NAME"]) is not str or len(data["PART_NAME"]) > 50:
            return jsonify("Data Error: Insufficient or invalid data for PART_NAME"), 400
        elif data["PART_PRICE"] == None or type(data["PART_PRICE"]) is not float:
            return jsonify("Data Error: Insufficient or invalid data  for PART_PRICE "), 400
        elif data["PART_TYPE"] == None or type(data["PART_TYPE"]) is not str or len(data["PART_TYPE"]) > 50:
            return jsonify("Data Error: Insufficient or invalid data for PART_TYPE"), 400

        dao = PartDAO()
        result = dao.insertPart(data)
        if result == 'Database Error: Duplicate data received, check submission data.':
            return'Database Error: Duplicate data received, check submission data.'
        elif result:
            return jsonify(result)
        else:
            return jsonify("Operation failed"), 405

    # Handler to update an existing part record in the database
    def updatePart(self, pid, data):
    
        # Check if at least one key-value pair is provided
        if not data:
            return jsonify("Data Error: Insufficient data. Please provide at least one key-value pair."), 400

        # If present validate PART_NAME 
        if "PART_NAME" in data:
            if data["PART_NAME"] == None or type(data["PART_NAME"]) is not str or len(data["PART_NAME"]) > 50:
                return jsonify("Data Error: Insufficient or invalid data for PART_NAME"), 400
        # If present validate PART_PRICE 
        if "PART_PRICE" in data:
            if data["PART_PRICE"] == None or type(data["PART_PRICE"]) is not float:
                return jsonify("Data Error: Insufficient or invalid data for PART_PRICE"), 400
        # If present validate PART_TYPE 
        if "PART_TYPE" in data:
            if data["PART_TYPE"] == None or type(data["PART_TYPE"]) is not str or len(data["PART_TYPE"]) > 50:
                return jsonify("Data Error: Insufficient or invalid data for PART_TYPE"), 400
        else:
            return jsonify("Key Error: Insufficient or invalid data"), 400
        
        # Keys and Values validated proceed to query
        dao = PartDAO()
        result = dao.updatePart(pid, data)
        
        if result == f"Part with ID:{pid} does not exist.":
            return jsonify(result)
        elif result:
            return jsonify(f"Part with ID:{pid} has been updated.", result)
        else:
            return jsonify("Operation failed"), 405
        
    # Handler to delete an existing part from the database
    def deletePart(self, pid):
        
        dao = PartDAO()
        result = dao.deletePart(pid)
        
        if result == f"Part with ID:{pid} does not exist.":
            return jsonify(result)
        elif result:
            return jsonify(f"Part with ID:{pid} has been deleted.")
        else:
            return jsonify("Operation failed"), 405