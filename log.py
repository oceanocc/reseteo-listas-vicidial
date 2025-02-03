
import datetime

def Log(file_log, message):
    now = datetime.datetime.now()
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
    file = open(file_log, "a")
    file.write("[" + datetime_str + "] " + message + "\n")
    file.close()
    print("[" + datetime_str + "] " + message)
