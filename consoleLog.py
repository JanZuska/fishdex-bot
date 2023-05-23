import datetime

def ConsoleLog(user):
    current_date_time: datetime.datetime = datetime.datetime.now()
    formated_date_time: str = current_date_time.strftime("%d.%m.%Y | %H:%M:%S")
    print(f"{formated_date_time} | {user} used command fishdex")