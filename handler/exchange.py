from flask import jsonify
from dao import ExchangeDAO, TransactionsDAO, UserDAO, RacksDAO, SuppliesDAO, SuppliersDAO, WarehousesDAO, PartDAO

class ExchangeHandler:
    # Mapping query output to dictionary to return to user
    def mapToDict(self, t):
        dict = {}
        dict['id'] = t[0]
        dict['record id'] = t[1]
        dict['quantity'] = t[2]
        dict['part'] = t[3]
        dict['Supplying Warehouse'] = t[4]
        dict['Supplying User'] = t[5]
        return dict
    
    # Handler function to get all Exchange transactions from database
    def getAllExchange(self):
        dao = ExchangeDAO()
        db_tuples = dao.getAllExchange()
        result = []
        for e in db_tuples:
            result.append(self.mapToDict(e))
        return jsonify(result)
    
    # Handler function to get Exchange transaction with specific id from database
    def searchById(self, pid):
        dao = ExchangeDAO()
        result = dao.searchById(pid)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify("Record Not Found"), 404
        
    # Handler to insert a new Exchange transaction into database 
    def insertExchange(self, data):
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
            elif data["TRANS_WARE_SUPPLIER"] == None or type(data["TRANS_WARE_SUPPLIER"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data"), 400
            elif data["SUPPLIER_USER_ID"] == None or type(data["SUPPLIER_USER_ID"]) is not int:
                return jsonify("Data Error: Insufficient or invalid data"), 400
        except KeyError:
            return jsonify("Key Error: Insufficient or invalid data"), 400
        # Constraint Validation
        # Transaction Type
        if data["TRANS_TYPE"] != "EXCHANGE":
            return jsonify("Data Error: Invalid transaction type"), 400
        # Warehouse Constraints
        warehouse_dao = WarehousesDAO()
        warehouse_supp_dao = WarehousesDAO()
        warehouse_data = warehouse_dao.searchById(data["WARE_ID"])
        warehouse_supp_data = warehouse_supp_dao.searchById(data["TRANS_WARE_SUPPLIER"])
        # Validate warehouses exist
        if warehouse_data == None:
            return jsonify("Invalid Operation: Requesting warehouse does not exist"), 405
        if warehouse_supp_data == None:
            return jsonify("Invalid Operation: Supplying warehouse does not exist"), 405
        # Referencing 2 Different Warehouses properly
        if data["TRANS_WARE_SUPPLIER"] == data["WARE_ID"]:
            return jsonify("Data Error: Must reference two different warehouses, a recipient and a supplier"), 400
        # Part Constraints
        parts_dao = PartDAO()
        parts_data = parts_dao.searchById(data["TRANS_PART"])
        if parts_data == None:
            return jsonify("Invalid Operation: Part does not exist"), 405
        # Validate warehouse budget
        trans_cost = parts_data[2] * data["TRANS_QTY"]
        budget = warehouse_data[2]
        budget_supp = warehouse_supp_data[2] 
        if budget < trans_cost:
            return jsonify("Invalid Operation: Insufficient warehouse budget"), 405
        # User Constraints
        user_dao = UserDAO()
        user_supp_dao = UserDAO()
        user_data = user_dao.searchById(data["USER_ID"])
        user_supp_data = user_supp_dao.searchById(data["SUPPLIER_USER_ID"])
        # Validate Users Exist
        if user_data == None:
            return jsonify("Invalid Operation: Requesting User does not exist"), 405
        if user_supp_data == None:
            return jsonify("Invalid Operation: Supplying user does not exist"), 405
        # Validate requesting user belongs to the requesting warehouse
        if user_data[5] != data["WARE_ID"]:
            return jsonify("Invalid Operation: Recipient User does not belong to requesting warehouse"), 405
        # Validate supplying user belongs to supplying warehouse
        if user_supp_data[5] != data["TRANS_WARE_SUPPLIER"]:
            return jsonify("Invalid Operation: Supplying user does not exist at supplying warehouse"), 405
        # Rack Constraints
        rack_dao = RacksDAO()
        rack_supp_dao = RacksDAO()
        rack_data = rack_dao.searchById(data["RACK_ID"])
        rack_supp_data = rack_supp_dao.searchByWareAndPartId(data["TRANS_WARE_SUPPLIER"], data["TRANS_PART"])
        # Validate rack with correct part exists
        if rack_data == None:
            return jsonify("Invalid Operation: Rack does not exist"), 405
        if rack_supp_data == None:
            return jsonify("Invalid Operation: Supplying rack does not exist"), 405
        # Validate recipient rack exists in warehouse
        if rack_data[4] != data["WARE_ID"]:
            return jsonify("Invalid Operation: Rack does not belong to recipient warehouse"), 405
        # Validate recipient rack holds correct part
        if rack_data[3] != data["TRANS_PART"]:
            return jsonify("Invalid Operation: Incorrect Rack for Part"), 405
        # Validate supplying rack holds correct part
        # Validate recipient rack has enough capacity and supplying rack has enough stock
        rack_cap = rack_data[1] - rack_data[2]
        rack_supp_stock = rack_supp_data[2]
        #print(rack_cap)
        #print(rack_supp_stock)
        # Rack Capacity
        if data["TRANS_QTY"] > rack_cap:
            return jsonify(f'Invalid Operation: Transaction quantity exceeds recipient rack capacity of: {rack_cap}'), 405
        # Rack Stock
        if data["TRANS_QTY"] > rack_supp_stock:
            return jsonify(f'Invalid Operation: Transaction quantity exceeds supplying rack stock of: {rack_supp_stock}'), 405
        # End of Validation for request data
        # Insert data to transactions
        dao = TransactionsDAO()
        record = dao.insertTransaction(data)
        if type(record) is not int:
            return jsonify("Inserting transaction record failed"), 400
        # Insert data to trans_exchange
        dao = ExchangeDAO()
        result = dao.insertExchange(record, data)
        if result:
            # Update affected tables upon successful transaction
            # Update Recipient Rack Stock
            rack_dao = RacksDAO()
            updated_rack_stock = rack_data[2] + data["TRANS_QTY"]
            rack_id = rack_data[0]
            rack_dict = {"RACK_STOCK" : updated_rack_stock}
            rack_update = rack_dao.updateRack(rack_id, rack_dict)
            print(rack_update)
            # Update Supplying Rack Stock
            rack_dao = RacksDAO()
            updated_rack_stock = rack_supp_data[2] - data["TRANS_QTY"]
            rack_id = rack_supp_data[0]
            rack_dict = {"RACK_STOCK" : updated_rack_stock}
            rack_update = rack_dao.updateRack(rack_id, rack_dict)
            print(rack_update)
            # Update Supplying Warehouse Budget
            warehouse_supp_dao = WarehousesDAO()
            updated_budget_supp = budget_supp + trans_cost
            ware_id_supp = warehouse_supp_data[0]
            ware_dict_supp = {"WARE_BUDGET" : updated_budget_supp}
            ware_update_supp = warehouse_supp_dao.updateWarehouse(ware_id_supp, ware_dict_supp)
            print(ware_update_supp)
            # Update Recipient Budget
            warehouse_dao = WarehousesDAO()
            updated_budget = budget - trans_cost
            ware_id = warehouse_data[0]
            ware_dict = {"WARE_BUDGET" : updated_budget}
            ware_update = warehouse_dao.updateWarehouse(ware_id, ware_dict)
            print(ware_update)
            return jsonify(result)
        else:
            return jsonify("Operation failed"), 405
        
    # Handler to update an existing Exchange transaction record in the database
    def updateExchange(self, data):
        # Code needed
        dao = ExchangeDAO()
        result = dao.updateExchange(data)
        # Code needed (maybe)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify("Operation failed"), 405
        