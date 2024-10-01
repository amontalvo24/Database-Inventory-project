from flask import jsonify
from dao import SuppliersDAO

class SuppliersHandler:
    
    # Mapping query output to dictionary to return to user
    def mapToDict(self, t):
        dict = {}
        dict['supplier_id'] = t[0]
        dict['supp_name'] = t[1]
        dict['supp_street'] = t[2]
        dict['supp_city'] = t[3]
        dict['supp_country'] = t[4]
        dict['supp_zipcode'] = t[5]
        return dict
    
    # Handler function to get all suppliers from database
    def getAllSuppliers(self):
        dao = SuppliersDAO()
        db_tuples = dao.getAllSuppliers()
        result = []
        for e in db_tuples:
            result.append(self.mapToDict(e))
        return jsonify(result)
    
    # Handler function to get supplier with specific id from database
    def searchById(self, supplier_id):
        dao = SuppliersDAO()
        result = dao.searchById(supplier_id)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify("Supplier Not Found"), 404
        
    # Handler to insert a new supplier into database 
    def insertSupplier(self, data):
        if "SUPPLIER_NAME" not in data or "SUPPLIER_STREET" not in data or "SUPPLIER_CITY" not in data or "SUPPLIER_COUNTRY" not in data or "SUPPLIER_ZIPCODE" not in data:
            return jsonify("Key Error: Insufficient or invalid data"), 400            
        if data["SUPPLIER_NAME"] == None or type(data["SUPPLIER_NAME"]) is not str or len(data["SUPPLIER_NAME"]) > 50:
            return jsonify("Data Error: Insufficient or invalid data for SUPPLIER_NAME"), 400
        elif data["SUPPLIER_STREET"] == None or type(data["SUPPLIER_STREET"]) is not str or len(data["SUPPLIER_STREET"]) > 100:
            return jsonify("Data Error: Insufficient or invalid data  for SUPPLIER_STREET "), 400
        elif data["SUPPLIER_CITY"] == None or type(data["SUPPLIER_CITY"]) is not str or len(data["SUPPLIER_CITY"]) > 50:
            return jsonify("Data Error: Insufficient or invalid data for SUPPLIER_CITY"), 400
        elif data["SUPPLIER_COUNTRY"] == None or type(data["SUPPLIER_COUNTRY"]) is not str or len(data["SUPPLIER_COUNTRY"]) > 50:
            return jsonify("Data Error: Insufficient or invalid data for SUPPLIER_COUNTRY"), 400
        elif data["SUPPLIER_ZIPCODE"] == None or type(data["SUPPLIER_ZIPCODE"]) is not str or len(data["SUPPLIER_ZIPCODE"]) > 20:
            return jsonify("Data Error: Insufficient or invalid data for SUPPLIER_ZIPCODE"), 400
        
        dao = SuppliersDAO()
        result = dao.insertSupplier(data)
        if result == f'Database Error: Duplicate data received, check submission data.':
            return jsonify(result)
        elif result:
            return jsonify(result)
        else:
            return jsonify("Operation failed"), 405
        
    # Handler to update an existing supplier record in the database
    def updateSupplier(self, supplier_id, data):
        # Check if at least one key-value pair is provided
        if not data:
            return jsonify("Data Error: Insufficient data. Please provide at least one key-value pair."), 400

        # If present validate SUPPLIER_NAME 
        if "SUPPLIER_NAME" in data:
            if data["SUPPLIER_NAME"] == None or type(data["SUPPLIER_NAME"]) is not str or len(data["SUPPLIER_NAME"]) > 50:
                return jsonify("Data Error: Insufficient or invalid data for SUPPLIER_NAME"), 400
        # If present validate SUPPLIER_STREET 
        if "SUPPLIER_STREET" in data:
            if data["SUPPLIER_STREET"] == None or type(data["SUPPLIER_STREET"]) is not str or len(data["SUPPLIER_STREET"]) > 100:
                return jsonify("Data Error: Insufficient or invalid data for SUPPLIER_STREET"), 400
        # If present validate SUPPLIER_CITY 
        if "SUPPLIER_CITY" in data:
            if data["SUPPLIER_CITY"] == None or type(data["SUPPLIER_CITY"]) is not str or len(data["SUPPLIER_CITY"]) > 50:
                return jsonify("Data Error: Insufficient or invalid data for SUPPLIER_CITY"), 400
        # If present validate SUPPLIER_COUNTRY
        if "SUPPLIER_COUNTRY" in data:
            if data["SUPPLIER_COUNTRY"] == None or type(data["SUPPLIER_COUNTRY"]) is not str or len(data["SUPPLIER_COUNTRY"]) > 50:
                return jsonify("Data Error: Insufficient or invalid data for SUPPLIER_COUNTRY"), 400
        # If present validate SUPPLIER_ZIPCODE
        if "SUPPLIER_ZIPCODE" in data:
            if data["SUPPLIER_ZIPCODE"] == None or type(data["SUPPLIER_ZIPCODE"]) is not str or len(data["SUPPLIER_ZIPCODE"]) > 20:
                return jsonify("Data Error: Insufficient or invalid data for SUPPLIER_ZIPCODE"), 400
        else:
            return jsonify("Key Error: Insufficient or invalid data"), 400
        
        dao = SuppliersDAO()
        result = dao.updateSupplier(data, supplier_id)
        if result == 'Database Error: duplicate data recieved, check submission data.':
            return jsonify(result)
        elif result == 'Database Error: Invalid supplier id':
            return jsonify(result)
        elif result:
            return jsonify(f"supplier {supplier_id} has been updated.", result)
        else:
            return jsonify("Operation failed"), 405
        
    # Handler to delete an existing supplier from the database
    def deleteSupplier(self, supplier_id):
        # Code needed
        dao = SuppliersDAO()
        result = dao.deleteSupplier(supplier_id)
        if result == f"Supplier {supplier_id} does not exist!":
            return jsonify(result) 
        elif result:
            return jsonify(f"Supplier {supplier_id} has been deleted.")
        else:
            return jsonify("Operation failed"), 405