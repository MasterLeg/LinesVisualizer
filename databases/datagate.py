from databases.dbpouch import DBPouch
from databases.dbstarted import DBStarted


class DataGate:

    def __init__(self):

        self.db_SSL1_started = DBStarted(kind='Started',
                                         line='SSL1',
                                         host='10.156.8.3',
                                         database='qiastatdxssl',
                                         user='pilot',
                                         password='READStat2020',
                                         table='serialnumber',
                                         time_field='Time'
                                         )

        self.db_SSL3_started = DBStarted(kind='Started',
                                         line='SSL1',
                                         host='10.156.12.33',
                                         database='qiastatdxssl',
                                         user='pilot',
                                         password='READStat2020',
                                         table='serialnumber',
                                         time_field='Time'
                                         )

        self.db_SSL1_finished = DBPouch(kind='Finished',
                                        line='SSL1',
                                        host='10.156.9.72',
                                        database='qiastatdxssl',
                                        user='pilot',
                                        password='READStat2020',
                                        table='pouch',
                                        time_field='Date')

        self.db_SSL3_finished = DBPouch(kind='Finished',
                                        line='SSL3',
                                        host='10.156.12.27',
                                        database='qiastatdxssl',
                                        user='pilot',
                                        password='READStat2020',
                                        table='pouch',
                                        time_field='Date')

        self.databases = {'SSL1': {'Started': self.db_SSL1_started,
                                   'Finished': self.db_SSL1_finished},
                          'SSL3': {'Started': self.db_SSL3_started,
                                   'Finished': self.db_SSL3_finished}}