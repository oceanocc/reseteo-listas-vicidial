 

import mysql.connector
from log import Log

db = mysql.connector.connect(host="187.188.251.231", user="cron", passwd="1234", db="asterisk", port="3308")

cursor = db.cursor()

query = """
    SELECT vc.dialable_leads 
    FROM vicidial_campaign_stats vc
    WHERE vc.campaign_id = '7777'
"""
cursor.execute(query)
rows = cursor.fetchall()

dialable_leads = rows[0][0]

# if dialable_leads < 1000:
if True:
    Log("/var/log/reseteo-listas/log", "Menos de 1k de registros, reseteando (" + str(dialable_leads) + "): ")

    query = """
        UPDATE vicidial_lists S
        SET resets_today=(resets_today + 1)
        WHERE
            S.campaign_id='7777'
            AND S.active = 'Y'
    """

    cursor.execute(query)
    query = """
        UPDATE vicidial_list L 
        JOIN vicidial_lists S on S.list_id=L.list_id
        SET called_since_last_reset = 'N'
        WHERE
            S.campaign_id='7777'
            AND S.active = 'Y'
            AND called_since_last_reset = 'Y'
    """
    cursor.execute(query)
