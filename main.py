from dotenv import load_dotenv
import mysql.connector
from log import Log
import os
import datetime

# Load .env variables
load_dotenv()

# Variables
host = os.getenv('host')
user = os.getenv('user')
passwd = os.getenv('passwd')
db = os.getenv('db')
port = os.getenv('port')

print(passwd)

db = mysql.connector.connect(host=host, user=user, passwd=passwd, db=db, port=port)

cursor = db.cursor()

query = """
    SELECT vc.dialable_leads 
    FROM vicidial_campaign_stats vc
    WHERE vc.campaign_id = 'C1'
"""
cursor.execute(query)
rows = cursor.fetchall()

dialable_leads = rows[0][0]

if dialable_leads < 1000:
    Log("/var/log/reseteo-listas-vicidial/log", "Menos de 1k de registros, reseteando C1 (" + str(dialable_leads) + "): ")

    # Update resets_today
    query = """
        UPDATE vicidial_lists S
        SET resets_today=(resets_today + 1)
        WHERE
            S.campaign_id='C1'
            AND S.active = 'Y'
    """

    # Update called_since_last_reset
    cursor.execute(query)
    query = """
        UPDATE vicidial_list L 
        JOIN vicidial_lists S on S.list_id=L.list_id
        SET called_since_last_reset = 'N'
        WHERE
            S.campaign_id='C1'
            AND S.active = 'Y'
            AND called_since_last_reset = 'Y'
    """
    cursor.execute(query)
else:
    now = datetime.datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
    print("[" + datetime_str + "] " + str(dialable_leads) + " registros disponibles")
