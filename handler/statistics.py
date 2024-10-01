from flask import jsonify
from dao import WarehousesDAO
from dao import StatisticsDAO
from handler import RacksHandler
class StatisticHandler:

        # Mapping query output to dictionary to return to user
    def mapToDict(self, t):
        dict = {}
        dict['id'] = t[0]
        dict['rack_id'] = t[1]
        return dict
    
    # Local Statistic Handlers
    def calculate_profit_by_year(self, wid):
        dao = StatisticsDAO()
        result = dao.calculate_profit_by_year(wid)
        if result:
            return jsonify(result)
        else:
            return jsonify("Insufficient Incoming and Outgoing transaction data from this warehouse")

    def get_top_5_racks_under_threshold(self, wid):
        dao = StatisticsDAO()
        result = dao.get_top_5_racks_under_threshold(wid)
        if len(result) == 0:
            return jsonify('No racks with quantities under 25% capacity in this warehouse'), 404
        else:
            return jsonify(result)

    def top_5_expensive_racks(self, wid):
        dao = StatisticsDAO()
        top = dao.top_5_expensive_racks(wid)
        if top:
            return jsonify(top)
        else:
            return jsonify("No Racks found in this Warehouse"), 404

    def get_top_3_supplier_trans(self, wid):
        dao = StatisticsDAO()
        result = dao.get_top_3_supplier_trans(wid)
        if len(result) == 0:
            return jsonify('Warehouse does not exist'), 404
        else:
            return jsonify(result)

    def get_bottom_3_parts_type(self, wid):
        dao = StatisticsDAO()
        result = dao.get_bottom_3_parts_type(wid)
        if len(result) == 0:
            return jsonify('Warehouse does not exist'), 404
        else:
            return jsonify(result)

    def get_bottom_3_days_smallest_incoming_price(self, wid):
        dao = StatisticsDAO()
        result = dao.get_bottom_3_days_smallest_incoming_price(wid)
        if len(result) == 0:
            return jsonify('Warehouse does not exist'), 404
        else:
            return jsonify(result)

    def get_top_3_users_most_exchanges(self, wid):
        dao = StatisticsDAO()
        result = dao.get_top_3_users_most_exchanges(wid)
        if len(result) == 0:
            return jsonify('Warehouse does not exist'), 404
        else:
            return jsonify(result)
    
    # Global Statistic Handler

    def get_top_10_warehouses_most_racks(self):
        dao = StatisticsDAO()
        result = dao.get_top_10_warehouses_most_racks()
        return jsonify(result)

    def get_top_5_warehouses_most_incoming_trans(self):
        dao = StatisticsDAO()
        result = dao.get_top_5_warehouses_most_incoming_trans()
        return jsonify(result)

    def get_top_5_warehouses_most_deliveries_exchanges(self):
        dao = StatisticsDAO()
        result = dao.get_top_5_warehouses_most_deliveries_exchanges()
        return jsonify(result)

    def get_top_3_users_most_trans(self):
        dao = StatisticsDAO()
        result = dao.get_top_3_users_most_trans()
        return jsonify(result)

    def get_top_3_warehouses_least_outgoing_trans(self):
        dao = StatisticsDAO()
        result = dao.get_top_3_warehouses_least_outgoing_trans()
        return jsonify(result)

    def get_top_3_warehouses_cities_most_trans(self):
        dao = StatisticsDAO()
        result = dao.get_top_3_warehouses_cities_most_trans()
        return jsonify(result)

    def parts_supplied_by_supplier(self, sid):
        dao = StatisticsDAO()
        result= dao.parts_supplied_by_supplier(sid)
        if len(result) == 0:
            return jsonify('Supplier ID does not exist or Supplier does not supply parts yet'), 404
        else:
            return jsonify(result)

    def transactions_by_warehouse(self, uid):
        dao = StatisticsDAO()
        result = dao.transactions_by_ware(uid)
        if len(result) == 0:
            return jsonify('This warehouse does not have transactions'), 404
        else:
          return jsonify(result)

    def parts_in_ware(self, wid):
        dao = StatisticsDAO()
        result = dao.parts_in_ware(wid)
        if len(result) == 0:
            return jsonify('This warehouse does not have parts'), 404
        else:
            return jsonify(result)
