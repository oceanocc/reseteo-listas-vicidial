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
limit_records = os.getenv('limit_records')

db = mysql.connector.connect(host=host, user=user, passwd=passwd, db=db, port=port)
cursor = db.cursor()

campaigns = ['A1', 'A2', 'A4']

for campaign in campaigns:

    query = f"""
        SELECT vc.dialable_leads 
        FROM vicidial_campaign_stats vc
        JOIN vicidial_campaigns vc2 ON vc2.campaign_id = vc.campaign_id
        WHERE vc.campaign_id = '{campaign}' AND active = 'Y'
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    if len(rows) == 0:
        print(f"{campaign} inactiva")
        continue;
    
    dialable_leads = rows[0][0]

    if dialable_leads < int(limit_records):
        Log("/var/log/reseteo-listas-vicidial/log", f"Menos de {limit_records} de registros, reseteando {campaign} (" + str(dialable_leads) + "): ")

        # Update resets_today
        query = f"""
            UPDATE vicidial_lists S
            SET resets_today=(resets_today + 1)
            WHERE
                S.campaign_id='{campaign}'
                AND S.active = 'Y'
        """

        # Update called_since_last_reset
        cursor.execute(query)
        query = f"""
            UPDATE vicidial_list L 
            JOIN vicidial_lists S on S.list_id=L.list_id
            SET called_since_last_reset = 'N'
            WHERE
                S.campaign_id='{campaign}'
                AND S.active = 'Y'
                AND called_since_last_reset = 'Y'
        """
        cursor.execute(query)
    else:
        now = datetime.datetime.now()
        datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
        print("[" + datetime_str + "] " + str(dialable_leads) + " registros disponibles")
