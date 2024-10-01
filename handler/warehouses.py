from flask import jsonify
from dao import WarehousesDAO

class WarehouseHandler:
    
    # Mapping query output to dictionary to return to user
    def mapToDict(self, t):
        dict = {}
        dict['id'] = t[0]
        dict['name'] = t[1]
        dict['budget'] = t[2]
        dict['street'] = t[3]
        dict['city'] = t[4]
        dict['country'] = t[5]
        dict['zipcode'] = t[6]
        
        return dict
    # Handler function to get all warehouses from database
    def getAllWarehouses(self):
        dao = WarehousesDAO()
        db_tuples = dao.getAllWarehouses()
        result = []
        for e in db_tuples:
            result.append(self.mapToDict(e))
        return jsonify(result)
    
    # Handler function to get warehouse with specific id from database
    def searchById(self, pid):
        dao = WarehousesDAO()
        result = dao.searchById(pid)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify("Warehouse Not Found"), 404
        
    # Handler to insert a new warehouse into database 
    def insertWarehouse(self, data):
        if "WARE_NAME" not in data or "WARE_STREET" not in data or "WARE_CITY" not in data or "WARE_COUNTRY" not in data or "WARE_ZIPCODE" not in data or "WARE_BUDGET" not in data:
            return jsonify("Key Error: Insufficient or invalid data"), 400            
        if data["WARE_NAME"] == None or type(data["WARE_NAME"]) is not str or len(data["WARE_NAME"]) > 50:
            return jsonify("Data Error: Insufficient or invalid data for WARE_NAME"), 400
        elif data["WARE_STREET"] == None or type(data["WARE_STREET"]) is not str or len(data["WARE_STREET"]) > 100:
            return jsonify("Data Error: Insufficient or invalid data  for WARE_STREET"), 400
        elif data["WARE_CITY"] == None or type(data["WARE_CITY"]) is not str or len(data["WARE_CITY"]) > 50:
            return jsonify("Data Error: Insufficient or invalid data for WARE_CITY"), 400
        elif data["WARE_COUNTRY"] == None or type(data["WARE_COUNTRY"]) is not str or len(data["WARE_COUNTRY"]) > 50:
            return jsonify("Data Error: Insufficient or invalid data for WARE_COUNTRY"), 400
        elif data["WARE_ZIPCODE"] == None or type(data["WARE_ZIPCODE"]) is not str or len(data["WARE_ZIPCODE"]) > 20:
            return jsonify("Data Error: Insufficient or invalid data for WARE_ZIPCODE"), 400
        elif data["WARE_BUDGET"] == None or type(data["WARE_BUDGET"]) is not float:
            return jsonify("Data Error: Insufficient or invalid data for WARE_BUDGET"), 400
        
        dao = WarehousesDAO()
        result = dao.insertWarehouse(data)
        if result == f'Database Error: Duplicate data received, check submission data.':
            return jsonify(result)
        elif result:
            return jsonify(result)
        else:
            return jsonify("Operation failed"), 405

    # Handler to update an existing warehouse record in the database
    def updateWarehouse(self, wid, data):
        # Check if at least one key-value pair is provided
        if not data:
            return jsonify("Data Error: Insufficient data. Please provide at least one key-value pair."), 400

        # If present validate WARE_NAME 
        if "WARE_NAME" in data:
            if data["WARE_NAME"] == None or type(data["WARE_NAME"]) is not str or len(data["WARE_NAME"]) > 50:
                return jsonify("Data Error: Insufficient or invalid data for WARE_NAME"), 400
        # If present validate WARE_STREET 
        if "WARE_STREET" in data:
            if data["WARE_STREET"] == None or type(data["WARE_STREET"]) is not str or len(data["WARE_STREET"]) > 100:
                return jsonify("Data Error: Insufficient or invalid data for WARE_STREET"), 400
        # If present validate WARE_CITY 
        if "WARE_CITY" in data:
            if data["WARE_CITY"] == None or type(data["WARE_CITY"]) is not str or len(data["WARE_CITY"]) > 50:
                return jsonify("Data Error: Insufficient or invalid data for WARE_CITY"), 400
        if "WARE_COUNTRY" in data:
            if data["WARE_COUNTRY"] == None or type(data["WARE_COUNTRY"]) is not str or len(data["WARE_COUNTRY"]) > 50:
                return jsonify("Data Error: Insufficient or invalid data for WARE_COUNTRY"), 400
        if "WARE_ZIPCODE" in data:
            if data["WARE_ZIPCODE"] == None or type(data["WARE_ZIPCODE"]) is not str or len(data["WARE_ZIPCODE"]) > 20:
                return jsonify("Data Error: Insufficient or invalid data for WARE_ZIPCODE"), 400
        if "WARE_BUDGET" in data:
            if data["WARE_BUDGET"] == None or type(data["WARE_BUDGET"]) is not float:
                return jsonify("Data Error: Insufficient or invalid data for WARE_BUDGETS"), 400
        else:
            return jsonify("Key Error: Insufficient or invalid data"), 400

        dao = WarehousesDAO()
        result = dao.updateWarehouse(wid, data)
        
        if result == f"Warehouse with ID:{wid} does not exist.":
            return jsonify(result)
        elif result == 'Database Error: Duplicate data received, check submission data.':
            return jsonify(result)
        elif result:
            return jsonify(f"Warehouse with ID:{wid} has been updated.", result)
        else:
            return jsonify("Operation failed"), 405
        
    # Handler to delete an existing warehouse from the database
    def deleteWarehouse(self, wid):
        
        dao = WarehousesDAO()
        result = dao.deleteWarehouse(wid)
        if result == f"Warehouse with ID:{wid} does not exist.":
            return jsonify(result)
        elif result:
            return jsonify(f"Warehouse with ID:{wid} has been deleted.")
        else:
            return jsonify("Operation failed"), 405