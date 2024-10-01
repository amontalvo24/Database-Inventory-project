from flask import jsonify
from dao import SuppliesDAO
# Boilerplate Supplies Handler class, FUNCTIONS ARE NOT FULLY IMPLEMENTED
class SuppliesHandler:

    # Mapping query output to dictionary to return to user
    def mapToDict(self, t):
        dict = {}
        dict['supplies_id'] = t[0]
        dict['supplier_id'] = t[1]
        dict['part_id'] = t[2]
        dict['stock'] = t[3]

        return dict
    
    # Handler function to get all supplies from database
    def getAllSupplies(self):
        dao = SuppliesDAO()
        db_tuples = dao.getAllSupplies()
        result = []
        for e in db_tuples:
            result.append(self.mapToDict(e))
        return jsonify(result)
    
    # Handler function to get supplies with specific id from database
    def searchById(self, pid):
        dao = SuppliesDAO()
        result = dao.searchById(pid)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify("Supply Not Found"), 404
        
    # Handler to insert a new supplies record into database 
    def insertSupplies(self, data):

        if "SUPPLIER_ID" not in data or "PART_ID" not in data or "STOCK" not in data:
            return jsonify("Key Error: Insufficient or invalid data"), 400            
        if data["SUPPLIER_ID"] == None or type(data["SUPPLIER_ID"]) is not int:
            return jsonify("Data Error: Insufficient or invalid data for SUPPLIER_ID"), 400
        elif data["PART_ID"] == None or type(data["PART_ID"]) is not int:
            return jsonify("Data Error: Insufficient or invalid data  for PART_ID "), 400
        elif data["STOCK"] == None or type(data["STOCK"]) is not int:
            return jsonify("Data Error: Insufficient or invalid data for STOCK"), 400
        
        dao = SuppliesDAO()
        result = dao.insertSupplies(data)
        if result == 'Database Error: Duplicate data received, check submission data.':
            return jsonify(result)
        elif result == 'Database Error: Invalid supplier id or part id specified.':
            return jsonify(result)
        elif result:
            return jsonify(result)
        else:
            return jsonify("Operation failed"), 405
        
    # Handler to update an existing rack record in the database
        
    # Handler to update an existing supplies record in the database
    def updateSupplies(self, sid, data):
         # Check if at least one key-value pair is provided
        if not data:
            return jsonify("Data Error: Insufficient data. Please provide at least one key-value pair."), 400

        # If present validate SUPPLIER_ID 
        if "SUPPLIER_ID" in data:
            if data["SUPPLIER_ID"] == None or type(data["SUPPLIER_ID"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data for SUPPLIER_ID"), 400
        # If present validate PART_ID 
        if "PART_ID" in data:
            if data["PART_ID"] == None or type(data["PART_ID"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data for PART_ID"), 400
        # If present validate STOCK 
        if "STOCK" in data:
            if data["STOCK"] == None or type(data["STOCK"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data for STOCK"), 400
        
        else:
            return jsonify("Key Error: Insufficient or invalid data"), 400
        
        
        dao = SuppliesDAO()
        result = dao.updateSupplies(sid, data)
        
        if result == 'Database Error: Duplicate data received, check submission data.':
            return jsonify(result)
        elif result == 'Database Error: Invalid supplier id or part id specified':
            return jsonify(result)
        elif result:
            return jsonify(f"Supply with ID:{sid} has been updated.", result)
        else:
            return jsonify("Operation failed"), 405
        
    # Handler to delete an existing supplies from the database
    def deleteSupplies(self, sid):
        
        dao = SuppliesDAO()
        result = dao.deleteSupplies(sid)
        
        if result == f"Supply with ID {sid} does not exist.":
            return jsonify(result)
        elif result:
            return jsonify(f"Supply with ID:{sid} has been deleted.")
        else:
            return jsonify("Operation failed"), 405