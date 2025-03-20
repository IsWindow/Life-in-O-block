from modulefinder import test
import os
from dotenv import load_dotenv 
from discord.ui import View, Button
import discord
from discord.ext import commands
import json
import random as rand
import time

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
     with open(filename, 'w') as f:
        json.dump(data, f ,indent=4)

load_dotenv()  # Loads the .env file
TOKEN = os.getenv("BOT_TOKEN")  # Gets the bot token from the .env file

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()  # Syncs commands with Discord
        print(f"Synced {len(synced)} commands!")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    
    print(f"Bot is online as {bot.user}")

data = load_json("data.json")





@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    
    if "pls add me" in message.content.lower():
        print("ADD REQUEST DETECTED")
        await message.channel.send("Alr gimme a sec")

        if message.author.id in data["users"]:
            await message.channel.send("your already added")
        else:
            data["users"][message.author.id] = {"money": 0, "foods": [], "weapons": [], "health": 100, "damage": 5, "equipped": ["fist"]}
            save_json("data.json", data)
            print(f"NEW USER SAVED: {message.author.id}")
            print(f"NEW USER BALANCE: {data['users'][message.author.id]}")
            print(f"NEW USER HEALTH: {data['users'][message.author.id]["health"]}")
            await message.channel.send("you have now been added")
    if "bal" in message.content.lower():
        if message.author.id not in data["users"]:
            await message.channel.send("You dont have a balance")
        else:  
            user_bal = data["users"][message.author.id]["money"]
            print(type(user_bal))

            money_embed = discord.Embed(
                title="Your balance",
                description=f"{message.author.mention} \n Balance: ${user_bal}",
                color=discord.Color.green()
            )

            await message.channel.send(embed=money_embed)
    if "list" in message.content.lower():

        list_embed = discord.Embed(
            title="Commands",
            description="1. pls add me \n 2. bal \n 3. sign up \n 4. my food \n 5. my health, \n 6. my wep \n 7. equiped \n 8. my dmg"
        )
        await message.channel.send(embed=list_embed)
    if "my food" in message.content.lower():
        user_id = message.author.id

        if user_id not in data["users"]:
            await message.channel.send("You dont have account to store food yk ")
        elif user_id in data['users']:
            for food in data['users'][user_id]["foods"]:
                await message.channel.send(food)
        else:
            await message.channel.send("You dont have any food")
    if "my health" in message.content.lower():
        user_id = message.author.id
        await message.channel.send(f"Your health: {data["users"][user_id]["health"]}")
    if "my wep" in message.content.lower():
        user_id = message.author.id

        if user_id not in data["users"]:
            await message.channel.send("you dont have any weapons")
        else:
            for weapons in data["users"][user_id]['weapons']:
                await message.channel.send(weapons)   
    if "equiped"in message.content.lower():
        user_id = message.author.id

        if user_id not in data["users"]:
            await message.channel.send("you dont have anything equipped")
        else:
            await message.channel.send(f"you have: {data["users"][message.author.id]["equipped"]} equipped")
    if "my dmg" in message.content.lower():
        user_id = message.author.id
        if user_id not in data["users"]:
            await message.channel.send("you dont have any damage yk what i mean?")
        else:
            await message.channel.send(f"Your damage: {data['users'][user_id]["damage"]}")
            
                                              
@bot.tree.command(name="e_work", description="Work to earn money")
async def e_work(interaction: discord.Interaction):
    worked_money = rand.randint(1, 2) #! CHANGE LATER

    if interaction.user.id in data["users"]:
        print(f"Money before work: {data["users"][interaction.user.id]["money"]}")

        data["users"][interaction.user.id]["money"] += worked_money
        save_json("data.json", data)

        print(f"Money after work: {data["users"][interaction.user.id]["money"]}")


        await interaction.response.send_message(f"You have made ${worked_money}")

    else:
        await interaction.response.send_message("You dont have a balance")

class food_shop_button(View):
    def __init__(self):
        super().__init__()

        apple_button = Button(label="APPLE", style=discord.ButtonStyle.green)
        apple_button.callback = self.apple_button_method
        self.add_item(apple_button)

        chicken_button = Button(label="CHICKEN",style=discord.ButtonStyle.green)
        chicken_button.callback = self.chicken_button_method
        self.add_item(chicken_button)

    async def apple_button_method(self, interation: discord.Interaction):

        user_id = interation.user.id

        if user_id not in data["users"]:
            await interation.response.send_message(f"{interation.user.mention} does not have a balance")
        else:
            print("USER HAS A BALANCE")
            print("CHECKING BALANCE")
            if "apple" in data["users"][user_id]["foods"]:
                await interation.response.send_message("You already have an apple")
            else:
                if data["users"][user_id]["money"] > 50:
                    await interation.response.send_message("You bought the apple!")

                    print(f"USER AMOUNT BEFORE BUYING APPLE: {data["users"][user_id]["money"]}")
                    data["users"][user_id]["money"] -= 50
                    print("Money has been subtratced")
                    print(f"USER AMOUNT AFTER BUYING APPLE: {data["users"][user_id]["money"]}")
                    data["users"][user_id]["foods"].append("Apple")
                    save_json("data.json", data)

                else:
                    await interation.response.send_message("Your broke gng😭")
    async def chicken_button_method(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        if user_id not in data["users"]:
            await interaction.response.send_message(f"{interaction.user.mention} does not have a balance")
        else:
            print("USER HAS A BALANCE")
            print("CHECKING BALANCE")
            if "apple" in data["users"][user_id]["foods"]:
                await interaction.response.send_message("You already have a chicken")
                await interaction.followup("Greedy ahh")
            else:
                if data["users"][user_id]["money"] > 100:
                    await interaction.response.send_message("You bought a chicken!")

                    data["users"][user_id]["money"] -= 100
                    data["users"][user_id]["foods"].append("Chicken")
                    save_json("data.json", data)

                else:
                    await interaction.response.send_message("Your broke gng😭")
class weapons_shop_button(View):
    def __init__(self):
        super().__init__()

        shank_button = Button(label="SHANK", style=discord.ButtonStyle.red)
        shank_button.callback = self.shank_button_method
        self.add_item(shank_button)

    async def shank_button_method(self, interation: discord.Interaction):

        user_id = interation.user.id

        if user_id not in data["users"]:
            await interation.response.send_message(f"{interation.user.mention} does not have a balance")
        else:
            print("USER HAS A BALANCE")
            print("CHECKING BALANCE")
            if "Shank" in data["users"][user_id]["weapons"]:
                await interation.response.send_message("You already have an shank")
            else:
                if data["users"][user_id]["money"] > 500:
                    await interation.response.send_message("You bought the shank! (the opps better watch out)")

                    print(f"USER AMOUNT BEFORE BUYING SHANK: {data["users"][user_id]["money"]}")
                    data["users"][user_id]["money"] -= 500
                    print("Money has been subtratced")
                    print(f"USER AMOUNT AFTER BUYING SHANK: {data["users"][user_id]["money"]}")
                    data["users"][user_id]["weapons"].append("Shank")
                    save_json("data.json", data)

                else:
                    await interation.response.send_message("Your broke gng😭")
@bot.tree.command(name="food_shop", description="buy food for fun or to regain health")
async def food_shop(interaction: discord.Interaction):

    embed = discord.Embed(
        title="**SHOP**",
        description=f"**FOODS**: \n 1. Apple - $50 \n 2. Chicken - $100",
        color=discord.Color.green(),
    )

    await interaction.response.send_message(embed=embed, view=food_shop_button())


@bot.tree.command(name="weapon_shop", description="buy weapons to hurt the opps")
async def weapon_shop(interaction: discord.Interaction):

    embed = discord.Embed(
        title="**SHOP**",
        description=f"**FOODS**: \n 1. shank - $500 \n DMG: 10 \n 2. Bat - $70 (buy DLC for ts) \n DMG: 15",
        color=discord.Color.red(),
    )

    await interaction.response.send_message(embed=embed, view=weapons_shop_button())


@bot.tree.command(name="use_item", description="use an item")
async def use_item(interaction: discord.Interaction, item_use: str):
    user_id = interaction.user.id
    print(f"USER WANTS TO USE {item_use}")

    #! FOOD ITEMS
    if item_use == "Apple":
        if item_use not in data["users"][user_id]["foods"]:
            await interaction.response.send_message("You dont have an apple to use 💀")
        else:


            if item_use not in data["users"][user_id]["foods"]:
                await interaction.response.send_message("You dont have a apple to use 💀")
            else:
                data["users"][user_id]["health"] += 5
                save_json("data.json", data)

            if  data["users"][user_id]["health"] > 100:
                await interaction.response.send_message("Your full stop tryna eat more😭")
                data["users"][user_id]["health"] -= 5
                save_json("data.json", data)

            elif data["users"][user_id]["health"] <= 100:
                data["users"][user_id]["health"] -= 5
                data["users"][user_id]["foods"].remove(item_use)
                data["users"][user_id]["health"] += 5

                save_json("data.json", data)
                await interaction.response.send_message("You ate your apple")

    elif item_use == "Chicken":
        if item_use not in data["users"][user_id]["foods"]:
            await interaction.response.send_message("You dont have a chicken to use 💀")
        else:
            data["users"][user_id]["health"] += 10 #!Adding health to check
            save_json("data.json", data)

            if  data["users"][user_id]["health"] > 100:
                await interaction.response.send_message("Your full stop tryna eat more😭")
                data["users"][user_id]["health"] -= 10
                save_json("data.json", data)

            elif data["users"][user_id]["health"] <= 100:
                data["users"][user_id]["health"] -= 10   
                data["users"][user_id]["foods"].remove(item_use)
                data["users"][user_id]["health"] += 10

                save_json("data.json", data)
                await interaction.response.send_message("You ate your chicken")


    #! WEAPONS
    elif item_use == "Shank":
        if item_use not in data["users"][user_id]["weapons"]:
            await interaction.response.send_message("You dont have a shank to use 💀")
        else:
            data["users"][user_id]["damage"] -= data["users"][user_id]["damage"]
            print("Subracting")
            if data["users"][user_id]["damage"] == 0:
                print("test 1 passed")
                data["users"][user_id]["damage"] += 10
                save_json("data.json", data)
                print("saving * * *")
                print(f"REMOVING: {data["users"][user_id]["equipped"]}")
                
                #!CHECKING WHAT IS EQUIPED
                if "fist" in data["users"][user_id]["equipped"]:
                    data["users"][user_id]["equipped"].remove("fist")

                if "Shank" in data["users"][user_id]["equipped"]:
                    data["users"][user_id]["equipped"].remove("Shank")
                print("ITEM HAS BEEN REMOVED")
                
                #!ADDING ITEM AND REMOVING FROM LIST
                data["users"][user_id]["equipped"].append("Shank")
                data["users"][user_id]["weapons"].remove("Shank")
                save_json("data.json", data)

                await interaction.response.send_message("Your previous equipped weapon has been deleted (im not that good of a programmer gimme a break)")
            else:
                await interaction.response.send_message("Something went wrong srry")
                print("Something went wrong")
    else:
        await interaction.response.send_message("That is NOT a valid item gng😭 ")

@bot.tree.command(name="jump_the_opps", description="Jump your opps and deal damage to them")
async def jump_the_opps(interaction: discord.Interaction, member: discord.Member):
    user_id = interaction.user.id
    attacker_damage = data['users'][user_id]["damage"]
    target_health = data['users'][member.id]["health"]
    print(f"TARGET HEALTH: {data['users'][member.id]["health"]}")
    print(f"ATTACKER DAMAGE: {attacker_damage}")

    if member.id not in data["users"]:
        await interaction.response.send_message("User hasnt been added")
    else:
        print(f"TARGET HEALTH: {data['users'][member.id]["health"]}")
        print(f"ATTACKER DAMAGE: {attacker_damage}")

        data['users'][member.id]["health"] -= data['users'][user_id]["damage"]

        #!LOGS
        print("OPP HAS BEEN ATTACKED")
        save_json("data.json", data)
        print("Damage has been dealt")
        print(f"TARGET HEALTH TEST: {target_health}")


        if target_health <= 0:
            data["users"][member.id]["money"] == 0
            data["users"][member.id]["damage"] == 0
            data["users"][member.id]["health"] == 100

                #!CHECKING WHAT IS EQUIPED
            if "fist" in data["users"][user_id]["equipped"]:
                data["users"][user_id]["equipped"].remove("fist")
                save_json("data.json", data)

            elif "Shank" in data["users"][user_id]["equipped"]:
                data["users"][user_id]["equipped"].remove("Shank")
                save_json("data.json", data)

            save_json("data.json", data)

            if "Apple" in data["users"][member.id]["foods"]:
                data["users"][member.id]["foods"].remove("Apple")
                save_json("data.json", data)

            elif "Chicken" in data["users"][member.id]["foods"]:
                data["users"][member.id]["foods"].remove("Apple")     
                save_json("data.json", data)

            elif "Shank" in data["users"][member.id]["weapons"]:
                data["users"][member.id]["foods"].remove("Shank")  
                save_json("data.json", data)
            
            await interaction.response.send_message(f"{member.mention} died")

        else:
            await interaction.response.send_message(f"{member.mention} got jumped")

#?MODERATION COMMANDS   
@bot.tree.command(name="set_money", description="set a users money")
async def set_money(interaction: discord.Interaction, member: discord.Member, amount: int):
    target_id = member.id 
    allowed_list = [
        1341593061146497100 #Mikael
    ]

    if interaction.user.id not in allowed_list:
        await interaction.response.send_message("You dont have permisson to use ts command💔💔💔")
    else:
        if target_id not in data["users"]:
            await interaction.response.send_message("User doesnt have a balance")

        print(f"AMOUNT: {amount}")
        data["users"][target_id]["money"] -= data["users"][target_id]["money"]
        if data["users"][target_id]["money"] == 0:
            print("AMOUNT HAS BEEN SUBTRACTED")

            data["users"][target_id]["money"] += amount
            save_json("data.json", data)
            print("AMOUNT HAS BEEN SAVED")
        else:
            print("SOMETHING WENT WRONG")

        print(f"USER AMOUNT {data["users"][target_id]["money"]}")

        await interaction.response.send_message("Amount has been set!")

@bot.tree.command(name="set_health", description="set a users health")
async def set_money(interaction: discord.Interaction, member: discord.Member, amount: int):
    target_id = member.id 
    allowed_list = [
        1341593061146497100 #Mikael
    ]

    if interaction.user.id not in allowed_list:
        await interaction.response.send_message("You dont have permisson to use ts command💔💔💔")
    else:
        if amount > 100:
            await interaction.response.send_message("you cant have more than 100 health💔💔💔")
        else:
            if target_id not in data["users"]:
                await interaction.response.send_message("User doesnt have a health bar")

        print(f"AMOUNT: {amount}")
        data["users"][target_id]["health"] -= data["users"][target_id]["health"]
        if data["users"][target_id]["health"] == 0:
            print("AMOUNT HAS BEEN SUBTRACTED")

            data["users"][target_id]["health"] += amount
            save_json("data.json", data)
            print("AMOUNT HAS BEEN SAVED")
        else:
            print("SOMETHING WENT WRONG")

        print(f"USER AMOUNT {data["users"][target_id]["health"]}")

        await interaction.response.send_message("Health has been set!")


bot.run(TOKEN) 
