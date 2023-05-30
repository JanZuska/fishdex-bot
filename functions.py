import json
import datetime
import discord
import random
from PIL import Image

with open("assets/json/emoji.json", "r") as file:
    emoji: dict = json.load(file)
    file.close()

with open("assets/json/location.json", "r") as file:
    locations: dict = json.load(file)
    file.close()

class Get():
    @staticmethod
    def Emoji(emoji_name: str, directory: str = "baits") -> str:
        for name, value in emoji[directory].items():
            if name == emoji_name:
                return value

    @staticmethod
    def LocationName(location_id: int) -> str:
        for id, details in locations.items():
            if int(id) == int(location_id):
                return details["name"]
            
    @staticmethod        
    def LocationId(location: str) -> int:
        for id, details in locations.items():
            for key, value in details.items():
                if value != location:
                    break
                return int(id)
            
    @staticmethod        
    def BadgeId(location: str) -> str:
        for id, details in locations.items():
            for key, value in details.items():
                if value != location:
                    break
                return details["badge_id"]

    @staticmethod
    def LocationsList():
        locations_list = []
        for id, deatils in locations.items():
            locations_list.append(deatils["name"])
        return locations_list
    
def TodayIsInInterval(interval: str) -> bool:
    today = datetime.date.today()
    year_now = today.year
    interval_start = interval.split("-")[0]
    interval_end = interval.split("-")[1]
    start_date = datetime.date(year_now, int(interval_start.split(".")[0]), int(interval_start.split(".")[1]))
    enf_date = datetime.date(year_now, int(interval_end.split(".")[0]), int(interval_end.split(".")[1]))
    if start_date <= today <= enf_date:
        return True
    else: 
        return False

def FormatDate(date):
    dates = date.split("-")
    dates = [i.split(".") for i in dates]
    today = datetime.date.today()
    formated_date = []
    for d in dates:
        temp_date = datetime.date(year = today.year, month = int(d[0]), day = int(d[1]))
        temp_date = temp_date.strftime("%d.%m")
        formated_date.append(temp_date)
    return f"{formated_date[0]} - {formated_date[1]}"

async def FileCoding():
    now = datetime.datetime.now()
    current_time = now.strftime("%M%S%f")
    random_number = random.randint(100000, 1000000)
    return f"{current_time}_{random_number}"

async def change_hue(image, hue_shift):
    h = image.convert('HSV')
    h, s, v = h.split()
    if hue_shift < 0:
        hue_shift = (hue_shift * 0.8) * (180 / 255)
        h = h.point(lambda x: ((x + hue_shift ) % 256))
    elif hue_shift > 0:
        hue_shift = (hue_shift * 1.2) * (180 / 255)
        h = h.point(lambda x: ((x + hue_shift ) % 256))
    else:
        h = h.point(lambda x: ((x + hue_shift ) % 256))
    new_image = Image.merge('HSV', (h, s, v)).convert('RGBA')
    new_image.putalpha(image.getchannel('A'))
    return new_image

async def SaveImage(image, name):
    image.save(f"images/{name}")
    return

async def GetFile(filename: str, folder: str):
    if folder == "fish":
        filename = filename["id"]
    file_name = f"{filename}.png"
    file_path = f"images/{folder}/{file_name}"
    file = discord.File(file_path, filename = file_name)
    return file

def find_index_by_name(dictionaries, name):
    for index, dictionary in enumerate(dictionaries):
        if dictionary.get("name") == name:
            return index
    return None
    

