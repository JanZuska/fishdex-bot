import datetime

def Log(action, guild, channel, user, message):
    current_date_time: datetime.datetime = datetime.datetime.now()
    formated_date_time: str = current_date_time.strftime("%d.%m.%Y | %H:%M:%S")

    time = f"{formated_date_time}"
    guild = f"{guild}"
    channel = f"{channel}"
    user = f"{user}"
    command = f"fishdex"
    message = f"{message}"

    log = f"{action}: [{time}] Guild: {guild} | Channel: {channel} | User: {user} | Command: {command} | Message: {message}"

    print(log)

def Ready(bot_name, guilds):
    current_date_time: datetime.datetime = datetime.datetime.now()
    formated_date_time: str = current_date_time.strftime("%d.%m.%Y | %H:%M:%S")

    time = f"{formated_date_time}"
    bot_name = f"{bot_name}"
    guilds = f"{guilds}"

    log = f"[{time}] Bot is logged as {bot_name} | Guilds: {guilds}"

    print(log)

def Join(bot_name, guild):
    current_date_time: datetime.datetime = datetime.datetime.now()
    formated_date_time: str = current_date_time.strftime("%d.%m.%Y | %H:%M:%S")

    time = f"{formated_date_time}"
    bot_name = f"{bot_name}"
    guild_name = f"{guild.name}"
    guild_id = f"{guild.id}"

    log = f"[{time}] {bot_name} joined {guild_name} ({guild_id})"

    print(log)

def Leave(bot_name, guild):
    current_date_time: datetime.datetime = datetime.datetime.now()
    formated_date_time: str = current_date_time.strftime("%d.%m.%Y | %H:%M:%S")

    time = f"{formated_date_time}"
    bot_name = f"{bot_name}"
    guild_name = f"{guild.name}"
    guild_id = f"{guild.id}"

    log = f"[{time}] {bot_name} left {guild_name} ({guild_id})"

    print(log)
