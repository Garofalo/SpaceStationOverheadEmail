import requests
import smtplib
import time
from datetime import datetime

# Specific information, must change to your LAT, LONG, and Email
LAT = 40.428131
LONG = -79.690491
EMAIL = 'ok'
PASSWORD = 'OK'

# Determine Where the ISS is over the earth
def is_overhead():
    res = requests.get(url='http://api.open-notify.org/iss-now.json')
    res.raise_for_status()
    data = res.json()

    data_dict = {
        'iss_lat': float(data['iss_position']['latitude']),
        'iss_long' : float(data["iss_position"]["longitude"])
    }
    return LAT-5 <= data_dict['iss_lat'] <= LAT+5 and LONG - 5 <= data_dict['iss_long'] <= LONG+5

# Determine whether it is dark enough to see the ISS
def is_dark_out():
    params = {
        'lat': LAT,
        'lng': LONG,
        'formatted': 0,
    }

    res = requests.get(url='https://api.sunrise-sunset.org/json', params=params)
    res.raise_for_status()
    data = res.json()

    times = {
        'sunrise': int(data['results']['sunrise'].split("T")[1].split(":")[0]),
        'sunset' : int(data['results']['sunset'].split("T")[1].split(":")[0])
    }

    time_now = datetime.now().hour

    return time_now>= times['sunset'] or time_now <= times['sunrise']


#Check every five minutes and send email if both return true
while True:
    time.sleep(300)
    if is_dark_out() and is_overhead():
        connection = smtplib.SMTP("STMPPLACEHOLDER")
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg="Subject: It's here \n\n It's above you and dark outside"
        )