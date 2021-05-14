from databases.database import DataBase


class DBStarted(DataBase):

    def __init__(self, kind, line, host, database, user, password, table, time_field):
        super().__init__(kind, line, host, database, user, password, table, time_field)

    def get_cartridges_between_datetimes(self, start_hour, end_hour):
        """
        Gets the cartridges manufactured between te two dates introduced
        :param start_hour: [datetime] Starting hour to count
        :param end_hour: [datetime] End time to count
        :return: Manufactured cartridges quantity between the two dates
        """

        query = f"""
                 SELECT COUNT(DISTINCT SN)
                 FROM {self.table}
                 WHERE {self.time_field} BETWEEN '{start_hour}'
                 AND '{end_hour}'       
                 """
        one_hour_cartridges = self.execute_query_get_one(query)

        return one_hour_cartridges

    def get_split_hour_cartridges(self, now_unix, dates_unix_list):
        """
        Gets the cartridges manufactured in the current day. The increment is in 15 minutes.

        :param now_unix: [int] Current datetime in UNIX format and end date. F.Ex: datetime(2021, 4, 29, 12, 32) = 1619692092
        :return cartridges _per_hour: [list] Returns a list of ints on which each entry is the
        manufactured cartridges in that hour. F.Ex: [0, 0, 18, 43, 45, 29, ..., 41, 21, 22, 10]
        """

        start_date_unix = now_unix - 86400

        query = f"""
         SELECT UNIX_TIMESTAMP({self.time_field}) DIV 900 * 900 AS "time", count(SN) AS "ID"
         FROM {self.table}
         WHERE {self.time_field} BETWEEN FROM_UNIXTIME({start_date_unix}) 
         AND FROM_UNIXTIME({now_unix})
         GROUP BY 1
         ORDER BY UNIX_TIMESTAMP({self.time_field}) DIV 900 * 900;
         """

        collected_data = self.execute_query_get_all(query)
        # The answer is the date in Unix format and the quantity
        # now = datetime(2021, 4, 29, 11, 20) =>
        # dates = [datetime(2021, 4, 28, ), ..., datetime(2021, 4, 29, )
        # F.Ex:
        # +------------+------+
        # |       time |   ID |
        # +============+======+
        # | 1619599500 |   18 |
        # +------------+------+

        # Problem: if there are no values in the time range, the sql does not return a zero in that field
        # It requires to be populated with zeros. Precreate a vector. Then match the data.

        # Covert to a dictionary:
        collected_data_dict = dict(collected_data)

        cartridges_per_hour = []

        for date in dates_unix_list:

            try:
                cartridges_per_hour += [collected_data_dict[date]]

            except KeyError:
                # If not found add a zero
                cartridges_per_hour += [0]

        return cartridges_per_hour

    def get_last_cartridge_date(self):
        query = f"""
         SELECT MAX({self.time_field})
         FROM {self.table};
         """

        collected_data = self.execute_query_get_one(query)
        return collected_data

    def get_current_timestamp(self):
        query = f"""
         SELECT CURRENT_TIMESTAMP;
         """

        collected_data = self.execute_query_get_one(query)
        return collected_data
