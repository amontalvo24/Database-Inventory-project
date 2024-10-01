from flask import jsonify
from dao import IncomingDAO, TransactionsDAO, UserDAO, RacksDAO, SuppliesDAO, WarehousesDAO, PartDAO

class IncomingHandler:
    # Mapping query output to dictionary to return to user
    def mapToDict(self, t):
        dict = {}
        dict['id'] = t[0]
        dict['record id'] = t[1]
        dict['quantity'] = t[2]
        dict['part'] = t[3]
        dict['supplier'] = t[4]
        return dict
    
    # Handler function to get all incoming transactions from database
    def getAllIncoming(self):
        dao = IncomingDAO()
        db_tuples = dao.getAllIncoming()
        result = []
        for e in db_tuples:
            result.append(self.mapToDict(e))
        return jsonify(result)
    
    # Handler function to get incoming transaction with specific id from database
    def searchById(self, pid):
        dao = IncomingDAO()
        result = dao.searchById(pid)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify("Record Not Found"), 404
        
    # Handler to insert a new incoming transaction into database 
    def insertIncoming(self, data):
        print("Entered function.")
        # Data Validation for request data
        # Format Validation
        try:
            if data["USER_ID"] == None or type(data["USER_ID"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data"), 400
            elif data["TRANS_QTY"] == None or type(data["TRANS_QTY"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data"), 400
            elif data["TRANS_TYPE"] == None or type(data["TRANS_TYPE"]) is not str:
                return jsonify("Data Error: Insufficient or invalid data"), 400
            elif data["WARE_ID"] == None or type(data["WARE_ID"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data"), 400
            elif data["RACK_ID"] == None or type(data["RACK_ID"]) is not int: 
                return jsonify("Data Error: Insufficient or invalid data"), 400
            elif data["TRANS_PART"] == None or type(data["TRANS_PART"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data"), 400
            elif data["TRANS_SUPPLIER"] == None or type(data["TRANS_SUPPLIER"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data"), 400
        except KeyError:
            return jsonify("Key Error: Insufficient or invalid data"), 400
        # Constraint Validation
        # Transaction Type
        if data["TRANS_TYPE"] != "INCOMING": 
            return jsonify("Data Error: Invalid transaction type"), 400
        # Warehouse Constraints
        warehouse_dao = WarehousesDAO()
        warehouse_data = warehouse_dao.searchById(data["WARE_ID"])
        parts_dao = PartDAO()
        parts_data = parts_dao.searchById(data["TRANS_PART"])
        # Validate warehouses exist
        if warehouse_data == None:
            return jsonify("Invalid Operation: Warehouse does not exist"), 405
        # Validate Part exists
        if parts_data == None:
            return jsonify("Invalid Operation: Part does not exist"), 405
        # Validate warehouse budget
        trans_cost = parts_data[2] * data["TRANS_QTY"]
        budget = warehouse_data[2] 

        if budget < trans_cost:
            return jsonify("Invalid Operation: Insufficient warehouse budget"), 405
        # User Constraints
        user_dao = UserDAO()
        user_data = user_dao.searchById(data["USER_ID"])
        # Validate User Exists
        if user_data == None:
            return jsonify("Invalid Operation: User does not exist"), 405
        # Validate user belongs to the warehouse
        if user_data[5] != data["WARE_ID"]:
            return jsonify("Invalid Operation: User does not belong to warehouse"), 405
        # Rack Constraints
        rack_dao = RacksDAO()
        rack_data = rack_dao.searchById(data["RACK_ID"])
        # Validate rack exists
        if rack_data == None:
            return jsonify("Invalid Operation: Rack does not exist"), 405
        # Validate rack exists in warehouse
        if rack_data[4] != data["WARE_ID"]:
            return jsonify("Invalid Operation: Rack does not belong to warehouse"), 405
        # Validate rack holds correct part
        if rack_data[3] != data["TRANS_PART"]:
            return jsonify("Invalid Operation: Incorrect Rack for Part"), 405
        # Validate enough space in rack
        remaining_cap = rack_data[1] - rack_data[2]
        if data["TRANS_QTY"] > remaining_cap:
            return jsonify(f'Invalid Operation: Transaction quantity exceeds remaining rack capacity of {remaining_cap}'), 405
        # Supplies Constraints
        supplies_dao = SuppliesDAO()
        supplies_data = supplies_dao.searchBySupplierId(data["TRANS_SUPPLIER"])
        # Validate supplier supplies the part
        if supplies_data[1] != data["TRANS_SUPPLIER"]:
            return jsonify("Invalid Operation: Supplier does not provide part"), 405
        # Validate supplier has enough stock for order
        if supplies_data[3] < data["TRANS_QTY"]:
            return jsonify("Invalid Operation: Insufficient supplier stock"), 405
        # End of Validation for request data
        # Insert data to transactions
        dao = TransactionsDAO()
        record = dao.insertTransaction(data)
        print(record)
        if type(record) is not int:
            return jsonify("Inserting transaction record failed"), 400
        # Insert data to trans_incoming
        dao = IncomingDAO()
        result = dao.insertIncoming(record, data)
        if result:
            # Update affected tables upon successful transaction
            # Update Supplies Stock
            supplies_dao = SuppliesDAO()
            updated_supp_stock = supplies_data[3] - data["TRANS_QTY"]
            supp_id = supplies_data[0]
            supp_dict = {"STOCK" : updated_supp_stock}
            supp_update = supplies_dao.updateSupplies(supp_id, supp_dict)
            #print(supp_update)
            # Update Rack Stock
            rack_dao = RacksDAO()
            updated_rack_stock = rack_data[2] + data["TRANS_QTY"]
            rack_id = rack_data[0]
            rack_dict = {"RACK_STOCK" : updated_rack_stock}
            rack_update = rack_dao.updateRack(rack_id, rack_dict)
            #print(rack_update)
            # Update Budget
            warehouse_dao = WarehousesDAO()
            updated_budget = budget - trans_cost
            ware_id = warehouse_data[0]
            ware_dict = {"WARE_BUDGET" : updated_budget}
            ware_update = warehouse_dao.updateWarehouse(ware_id, ware_dict)
            #print(ware_update)
            return jsonify(result)
        else:
            return jsonify("Inserting incoming record failed"), 400
        
    # Handler to update an existing incoming transaction record in the database
    def updateIncoming(self, data):
        # Code needed
        dao = IncomingDAO()
        result = dao.updateIncoming(data)
        # Code needed (maybe)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify("Operation failed"), 405
        