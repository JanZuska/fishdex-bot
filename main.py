import discord
import json

with open("fishao-data.json", "r") as file:
    data = json.load(file)
    file.close()

def GetEmoji(key):
    for name, value in emoji.items():
        if name == key:
            return value

def GetLocationName(key):
    for id, name in locations.items():
        if int(id) == key:
            return name
        
def GetLocationId(key):
    for id, name in locations.items():
        if name == key:
            return id


def LocationsList():
    locations_list = []
    for id, name in locations.items():
        locations_list.append(name)
    return locations_list

async def GetFish(location_id):
    fish = []
    for one_fish in data:
        try:
          locations = one_fish["catch_req"]["location_ids"]
          if int(location_id) in locations:
              fish.append(one_fish["name"])
        except Exception as e:
          print(f"Error reading the price. Error: {e}")
    return fish

async def FishDetails(fish):
    for one_fish in data:
        try:
          name = one_fish["name"]
          if str(fish) == name:
              return one_fish
        except Exception as e:
          print(f"Error reading the data. Error: {e}")

async def GetFile(fish):
    fish_id = fish["id"]
    file_name = f"{fish_id}.png"
    file_path = f"images/fish/{file_name}"
    file = discord.File(file_path, filename = file_name)
    return file

async def BuildEmbed(fish):
    fish_name = fish["name"]
    fish_id = fish["id"]
    fish_rating = ""
    for i in range(int(fish["rating"])):
        fish_rating += f"{GetEmoji('star')} "
    fish_rarity_factor = fish["rarity_factor"]
    fish_catch_req = fish["catch_req"]
    fish_location = ""
    for location in fish_catch_req["location_ids"]:
        fish_location += f"{GetLocationName(location)} "
    fish_baits = ""
    for bait in fish_catch_req["bait_category"]:
        fish_baits += f"{GetEmoji(bait)} "
    fish_min_length = int(fish["min_length"]) + 1
    fish_avg_length = fish["avg_length"]
    fish_max_length = int(fish["max_length"]) - 1
    embed = discord.Embed(
        title = fish_name,
        description = "",
        color = discord.Colour.blurple(),

    )
    embed.add_field(name = "Rating:", value = f"{fish_rating} ({fish_rarity_factor})", inline = False)
    embed.add_field(name = "Location:", value = fish_location, inline = False)
    embed.add_field(name = "Baits:", value = fish_baits, inline = False)
    embed.add_field(name = "Min length:", value = fish_min_length, inline = True)
    embed.add_field(name = "Avg length:", value = fish_avg_length, inline = True)
    embed.add_field(name = "Max length:", value = fish_max_length, inline = True)
    embed.set_image(url = f"attachment://{fish_id}.png")
    return embed

bot = discord.Bot()

locations = {
1 : "Laketown",
2 : "Rio Tropical",
3 : "Pinheira Beach",
4 : "Cool Mountain",
5 : "Mystic Desert",
6 : "Sibiri City",
7 : "Aquayama",
8 : "Seagull Harbor",
9 : "Thombani Town",
10 : "Marshville",
11 : "Palm Island",
12 : "Lucky Raft",
101 : "Trour Farm",
104 : "Pyramid",
108 : "Lost Valley",
110 : "Little Rio",
111 : "Pirate Cave",
112 : "Club",
113 : "Factory",
201 : "Boat on Sea",
202 : "Lake Run",
203 : "Race",
204 : "Moray",
300 : "Backyard"
}
emoji = {
"hook" : "<:1:1099982706928005162>", 
"vegetal" : "<:2:1099982710287638619>",
"dough" : "<:3:1099982712099577936>",
"fish" : "<:5:1099982714901381132>",
"insects" : "<:10:1099982716159660034>", 
"meat" : "<:11:1099982718240030793>",
"lures" : "<:12:1099982720307822642>",
"shark" : "<:44:1099982721746468864>",
"prehistoric" : "<:45:1099982723856216114>",
"pelican" : "<:46:1099982724967694368>",
"monkfish" : "<:47:1099982727803043900>",
"star" : "<:48:1099982729925365790>",
"tuna" : "<:49:1099982732119003188>",
"marlin" : "<:50:1099982830685130795>",
"barracuda" : "<:51:1099982833159778376>",
"monster" : "<:52:1099982737768718346>",
"star" : "<:xp:1099982901325611118>"
}


class LocationSelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=location,description="") for location in LocationsList()]
        super().__init__(placeholder = "Choose a location!", options = options, min_values = 1, max_values = 1)

    async def callback(self, interaction): # the function called when the user is done selecting options
        await interaction.response.send_message(f"You chose {self.values[0]}")
        fish = await GetFish(GetLocationId(self.values[0]))
        if len(fish) > 25:
            fish = fish[0:24]
        await interaction.channel.send("Choose a fish!", view=Fish(fish))

class Location(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(LocationSelect())

class FishSelect(discord.ui.Select):
    def __init__(self, fish):
        options = [discord.SelectOption(label=one_fish,description="") for one_fish in fish]
        super().__init__(placeholder = "Choose a fish!", options = options, min_values = 1, max_values = 1)

    async def callback(self, interaction): # the function called when the user is done selecting options
        fish = await FishDetails(self.values[0])
        await interaction.response.send_message(file = await GetFile(fish), embed = await BuildEmbed(fish))


class Fish(discord.ui.View):
    def __init__(self, fish):
        super().__init__()
        self.add_item(FishSelect(fish))

@bot.command()
async def fishdex(ctx):
    await ctx.send("Choose a location!", view=Location())

bot.run("MTA3MDcwNDcxMzQ1ODI3NDM4NA.GKjVtM.HR3vmOwC7GZxwUIX9f334fijPUjk214CvISCQw")
