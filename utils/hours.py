from datetime import timedelta, datetime
import time


class Hours:

    def __init__(self):
        pass

    def get_datetime_hours_list(self, interval=15):
        """
        Creates a list of datetime (dates and hours) from the desired split by the interval introduced in minutes in the
        current date.
        F.Ex: interval = 15 minutes, now() = datetime(2021, 2, 4, 13, 32) => get_datetime_hours_array(15) =>
        [datetime(2021, 2, 3, 13, 15), datetime(2021, 2, 3, 13, 30), ..., datetime(2021, 2, 4, 13, 45)]
        :param interval: [int] Minutes to split the vector. F.EX: 15, the vector will be: [datetime(2021, 2, 2, 14, 00),
        datetime(2021, 2, 2, 14, 15), ... ]
        :return: [list: [datetime]] Returns the manufactured cartridges in the introduced date. + 2 extra data,
        the immediately previous and afterwards. F:Ex:
        [datetime(2021, 2, 3, 13, 15), datetime(2021, 2, 3, 13, 30), ..., datetime(2021, 2, 4, 13, 45)]
        """
        # Today datetime format
        today = datetime.today()
        # today = datetime(2021, 2, 3, 11, 31)

        # Current minutes
        current_minutes = today.minute

        # Rounded minutes
        rounded_minutes = (current_minutes // interval) * interval

        # End date (changing to rounded minutes)
        end_date = today.replace(minute=rounded_minutes, second=0, microsecond=0)

        # Start date (one day before)
        start_date = end_date - timedelta(days=1)

        # Quantity of minutes in a day (plus an extra query for the cartridges been manufactured right now)
        minutes_in_a_day = 24*60 + interval

        # Create hours list
        hours_list = [start_date + timedelta(minutes=i) for i in range(0, minutes_in_a_day, interval)]

        return hours_list

    def get_string_hours_list(self):
        """
        Converts the vector of a day (24 hours) split by the desrired interval into a list of df strings with the hours.
        Just returns o'clock values. The in between values, like 22:15 or 22:30, appear as void ('') to plot correctly.
        F.Ex: ['22:00', '', '', '', ..., '21:00', '', '', '', '22:00']
        Note: Start and end are the same value to recreate the grafana. Lokk that it starts by '22:00' and ends as well
        with '22:00'. The same applies to void values.
        :return: [list: [str]] List of str of the hours in the turn. F.Ex: ['22:00', '', '23:00', '', ..., ]
        """
        # Class method: the list of datetime objects used to query the data to the data base
        datetimes_list = self.get_datetime_hours_list(15)

        # Only if minute =  0, Add the hour, '12:00'
        hours = [date.strftime('%H:%M') if date.minute == 0 else '' for date in datetimes_list]

        return hours

    def last_hour(self, timestamp_now):
        """
        Get in datetime format last hour.
        datetime(2021, 5, 12, 15, 39, 31) => datetime(2021, 5, 12, 14, 0, 0)
        :param timestamp_now: [datetime] Current timestamp in the database
        :return:
        """
        last = datetime(timestamp_now.year, timestamp_now.month, timestamp_now.day, timestamp_now.hour) - timedelta(hours=1)
        return last

    def current_hour(self, timestamp_now):
        """
        Get in datetime format current hour.
        datetime(2021, 5, 12, 15, 39, 31) => datetime(2021, 5, 12, 15, 0, 0)
        :param timestamp_now: [datetime] Current timestamp in the database
        :return:
        """
        last = datetime(timestamp_now.year, timestamp_now.month, timestamp_now.day, timestamp_now.hour)
        return last

    def next_hour(self, timestamp_now):
        """
        Get in datetime format next hour.
        datetime(2021, 5, 12, 15, 39, 31) => datetime(2021, 5, 12, 16, 0, 0)
        :param timestamp_now: [datetime] Current timestamp in the database
        :return:
        """
        next = datetime(timestamp_now.year, timestamp_now.month, timestamp_now.day, timestamp_now.hour) + timedelta(hours=1)
        return next

    def datetime_to_unix(self, date):
        unixtime = int(time.mktime(date.timetuple()))
        return unixtime

    def now_unix(self):
        now = datetime.now()
        now_unix = self.datetime_to_unix(now)
        return now_unix

    def get_unix_dates_list(self):
        dates = self.get_datetime_hours_list(15)
        return [self.datetime_to_unix(date) for date in dates]