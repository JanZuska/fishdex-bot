import datetime
from colorama import init, Fore, Style

init()

EXECUTE = f"{Fore.GREEN}EXECUTE{Style.RESET_ALL}"
TIMEOUT = f"{Fore.YELLOW}TIMEOUT{Style.RESET_ALL}"
DEBUG = f"{Fore.BLUE}DEBUG{Style.RESET_ALL}"

def Log(action, guild, channel, user, message):
    current_date_time: datetime.datetime = datetime.datetime.now()
    formated_date_time: str = current_date_time.strftime("%d.%m.%Y | %H:%M:%S")

    time = f"{Fore.CYAN}{formated_date_time}{Style.RESET_ALL}"
    guild = f"{Fore.CYAN}{guild}{Style.RESET_ALL}"
    channel = f"{Fore.CYAN}{channel}{Style.RESET_ALL}"
    user = f"{Fore.CYAN}{user}{Style.RESET_ALL}"
    command = f"{Fore.CYAN}fishdex{Style.RESET_ALL}"
    message = f"{Fore.CYAN}{message}{Style.RESET_ALL}"

    log = f"{action}: [{time}] Guild: {guild} | Channel: {channel} | User: {user} | Command: {command} | Message: {message}"

    print(log)

def Ready(bot_name, guilds):
    current_date_time: datetime.datetime = datetime.datetime.now()
    formated_date_time: str = current_date_time.strftime("%d.%m.%Y | %H:%M:%S")

    time = f"{Fore.CYAN}{formated_date_time}{Style.RESET_ALL}"
    bot_name = f"{Fore.CYAN}{bot_name}{Style.RESET_ALL}"
    guilds = f"{Fore.CYAN}{guilds}{Style.RESET_ALL}"

    log = f"{DEBUG}: [{time}] Bot is logged as {bot_name} | Guilds: {guilds}"

    print(log)
