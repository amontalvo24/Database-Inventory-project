from flask import jsonify
from dao import RacksDAO
# Boilerplate Racks Handler class, FUNCTIONS ARE NOT FULLY IMPLEMENTED
class RacksHandler:

    # Mapping query output to dictionary to return to user
    def mapToDict(self, t):
        dict = {}
        dict['id'] = t[0]
        dict['capacity'] = t[1]
        dict['stock'] = t[2]
        dict['part_id'] = t[3]
        dict['ware_id'] = t[4]

        return dict
    
    # Handler function to get all racks from database
    def getAllRacks(self):
        dao = RacksDAO()
        db_tuples = dao.getAllRacks()
        result = []
        for e in db_tuples:
            result.append(self.mapToDict(e))
        return jsonify(result)
    
    # Handler function to get rack with specific id from database
    def searchById(self, pid):
        dao = RacksDAO()
        result = dao.searchById(pid)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify("Rack Not Found"), 404
        
    # Handler to insert a new rack into database 
    def insertRack(self, data):

        if "RACK_CAPACITY" not in data or "RACK_STOCK" not in data or "PART_ID" not in data or "WARE_ID" not in data:
            return jsonify("Key Error: Insufficient or invalid data"), 400            
        if data["RACK_CAPACITY"] == None or type(data["RACK_CAPACITY"]) is not int:
            return jsonify("Data Error: Insufficient or invalid data for RACK_CAPACITY"), 400
        elif data["RACK_STOCK"] == None or type(data["RACK_STOCK"]) is not int:
            return jsonify("Data Error: Insufficient or invalid data  for RACK_STOCK "), 400
        elif data["PART_ID"] == None or type(data["PART_ID"]) is not int:
            return jsonify("Data Error: Insufficient or invalid data for PART_ID"), 400
        elif data["WARE_ID"] == None or type(data["WARE_ID"]) is not int:
            return jsonify("Data Error: Insufficient or invalid data for WARE_ID"), 400
        
        dao = RacksDAO()
        result = dao.insertRack(data)
        if result == f'Database Error: Duplicate data received, check submission data.':
            return jsonify(result)
        elif result == 'Database Error: Invalid part id or warehouse id specified':
            return jsonify(result)
        elif result == 'Database Error: Stock exceeds rack capacity':
            return jsonify(result)
        elif result:
            return jsonify(result)
        else:
            return jsonify("Operation failed"), 405
        
    # Handler to update an existing rack record in the database
    def updateRack(self, rid, data):

        if "RACK_CAPACITY" not in data and "RACK_STOCK" not in data and "PART_ID" not in data and "WARE_ID" not in data:
            return jsonify("Key Error: Insufficient or invalid data"), 400   
        # If present validate RACK_CAPACITY 
        if "RACK_CAPACITY" in data:
            if data["RACK_CAPACITY"] == None or type(data["RACK_CAPACITY"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data for RACK_CAPACITY"), 400
        # If present validate RACK_STOCK 
        if "RACK_STOCK" in data:
            if data["RACK_STOCK"] == None or type(data["RACK_STOCK"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data for RACK_STOCK"), 400
        # If present validate PART_ID 
        if "PART_ID" in data:
            if data["PART_ID"] == None or type(data["PART_ID"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data for PART_ID"), 400
        # If present validate PART_TYPE 
        if "WARE_ID" in data:
            if data["WARE_ID"] == None or type(data["WARE_ID"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data for WARE_ID"), 400
        
        dao = RacksDAO()
        result = dao.updateRack(rid, data)
        
        if result:
            return jsonify(result)
        else:
            return jsonify("Operation failed"), 405
        
    # Handler to delete an existing rack from the database
    def deleteRack(self, rid):
        
        dao = RacksDAO()
        result = dao.deleteRack(rid)
        
        if result == f"Rack with ID:{rid} does not exist.":
            return jsonify(result)
        elif result:
            return jsonify(f"Rack with ID:{rid} has been successfully deleted.")
        else:
            return jsonify("Operation failed"), 405