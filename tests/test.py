import unittest
from databases.datagate import DataGate

from hours import Hours


class MyTestCase(unittest.TestCase):
    def test_something(self):
        dg = DataGate()
        db = dg.db_SSL3_finished
        hours = Hours()
        now_unix = hours.now_unix()
        dates_list = hours.get_datetime_hours_list(15)
        print('Horas normales: ', dates_list)
        dates_unix_list = hours.get_unix_dates_list()
        print('Nuevo vector horas: ', hours.get_unix_dates_list())

        cartridges = db.get_split_hour_cartridges(now_unix, dates_unix_list)
        print('Cantidad de cartruchos: ', cartridges)

        hours_list = hours.get_string_hours_list()
        print('Lista de las horas para los gráficos', hours_list)

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
