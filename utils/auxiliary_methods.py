from datetime import datetime

def transform_valuetodate_to_date(excel_date):
    """
    Transform from an Excel only understandable values to ISO date format
    The 44081 are the days far from 1st January 1900.
    The 0.627417 is the % from completing the day. Where 00:00h is 0%

    Example: 44081.627417 is in fact: 07/09/2020  15:03:29
    :return dt: (datetime) The date in format: dd/mm/yyyy hh:mm:ss
    """

    # Entry example: excel_date = 44052.4059375
    dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(excel_date) - 2)

    # Devuelvo sólo los decimales del número
    dec = excel_date % 1

    h = dec * 24
    # print('La hora es: ', h)

    m = (h % 1) * 60
    # print('Los minutos es: ', m)

    s = (m % 1) * 60
    # print('Los segundos son: ', round(s))

    try:
        dt = dt.replace(hour=int(h), minute=int(m), second=int(s))
        # print(dt)
    except Exception:
        print(f'Error en los valores: {h}, {m} y {s}')
    return dt


def transform_date_to_valuetodate(date1):
    """
    Transforms from a date format to the Julian Microsoft (Excel understandable) format.

    Example:
    [In] transform_date_to_valuetodate(2020-09-08 09:44:33.166154)  => [Out] 44052.4059375

    :param date1: [datetime] date desired to transform, F.Ex: 2020-09-08 09:44:33.166154
    :return: [float] Transformed date, F.Ex: 44052.4059375
    """
    temp = datetime(1899, 12, 30)  # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)


def tr_str_to_datetime(day):
    """
    Transforms a string into a datetime

    Example: '2020-09-02 00:00:01.00000' =>  [datetime] 2020-09-02 00:00:01

    :param day: [str] Desired date in ISO format (needs until microseconds)
    :return date_time_obj: [datetime] Desired date in datetime object format
    """
    try:
        date_time_obj = datetime.strptime(day, '%Y-%m-%d %H:%M:%S.%f')
    except:
        date_time_obj = datetime.strptime(day, '%Y-%m-%d %H:%M:%S')

    return date_time_obj


def get_increase_in_valuedate(increment):
    """
    Gets the valuedate form of the desired increment.
    :param increment: [int] Desired increment in minutes. F.Ex: 30 => 30 minutes, half an hour.
    :return delta: [float] Increment in datevalue form. F.Ex: 0.020833333335758653
    """
    # Transform first random starting date
    d1 = transform_date_to_valuetodate(datetime(2020, 9, 8, 0, 0))
    # Transform second random same date but added the increment
    d2 = transform_date_to_valuetodate(datetime(2020, 9, 8, 0, increment))
    # Get the difference (in valuedate format)
    delta = d2 - d1
    return delta
