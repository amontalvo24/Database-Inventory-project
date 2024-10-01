from flask import jsonify
from dao import TransactionsDAO

class TransactionsHandler:
    # Mapping query output to dictionary to return to user
    def mapToDict(self, t):
        dict = {}
        dict['id'] = t[0]
        dict['type'] = t[1]
        dict['date'] = t[2]
        dict['user_id'] = t[3]
        dict['ware_id'] = t[4]
        dict['rack_id'] = t[5]
        return dict
    
    # Handler function to get all transactions from database
    def getAllTransactions(self):
        dao = TransactionsDAO()
        db_tuples = dao.getAllTransactions()
        result = []
        for e in db_tuples:
            result.append(self.mapToDict(e))
        return jsonify(result)
    
    # Handler function to get transaction with specific id from database
    def searchById(self, pid):
        dao = TransactionsDAO()
        result = dao.searchById(pid)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify("Not Found"), 404
        
    # Handler to insert a new transaction record into database 
    def insertTransaction(self, data, helper):
        # Data Validation
        if "USER_ID" not in data:
            return jsonify("Insufficient Data"), 405
        if data["TRANS_QTY"] == None:
            return jsonify("Insufficient Data"), 405
        if data["TRANS_TYPE"] == None:
            return jsonify("Insufficient Data"), 405
        if data["USER_ID"] == None:
            return jsonify("Insufficient Data"), 405
        if data["WARE_ID"] == None:
            return jsonify("Insufficient Data"), 405
        if data["RACK_ID"] == None: 
            return jsonify("Insufficient Data"), 405
        
        dao = TransactionsDAO()
        record = dao.insertTransaction(data)
        if record is int:
            # Call corresponding handler based on transaction type
            return 
        
        if result is int:
            return jsonify(result)
        else:
            return jsonify("Operation failed"), 405
        
    # Handler to update an existing transaction record in the database
    def updateTransaction(self, data):
        # Code needed
        dao = TransactionsDAO()
        result = dao.updateTransaction(data)
        # Code needed (maybe)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify("Operation failed"), 405
        