import discord
import os
import requests
from discord.ext import commands
from supsdown import updown
from replit import db
import random
import asyncio
from hangman_game import HangmanGame, get_word_list, send_hangman_image
from guess import NumberGuessingGame

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='$', intents=intents)
bet_amount = 0
game_instance_number = NumberGuessingGame()
game_instance_supsdown = updown()
game_in_progress = False
word_list = get_word_list()
image_folder_path = 'images'
game_instance_hangman = HangmanGame(word_list,image_folder_path)
channel_id = 1225736957917925378
active_coin_drops = {}


@client.command()
async def hangman(ctx):
  global game_instance_hangman
  global game_in_progress
  
  if (game_in_progress):
    await ctx.send("A game is already in progress.")
    return
    
  game_instance_hangman.reset_game()
  await game_instance_hangman.get_current_state(ctx)
  game_in_progress = True
  
@client.command()
async def camelhelp(ctx):
  help_message = """
🐪 **Welcome to CamelBot's Command Help!** 🐪
Here's what you can do with CamelCoins:

1. 💰 **$addmoney [user] [amount]** - Add camel coins to your balance. (Admin only)
2. 🎲 **$bet [amount]** - Place your bet before starting a game.
3. 💼 **$balance** - Check your current camel coin balance.
4. 🎁 **$give [user] [amount]** - Share some camel coins with another user.
5. 👋 **$hello** - Greet the bot with a friendly message.
6. 🦹 **$steal [user] [amount]** - Attempt to snatch some camel coins from another user.
7. 🔢 **$number** - Start the Number Guessing Game.
8. 🎯 **$numberguess [number]** - Guess the number in the Number Guessing Game.
9. 🚪 **$numberexit** - Exit the Number Guessing Game.
10. 🃏 **$joke** - Get a random joke.
11. 🎲 **$supsdown** - Start the 7 Up 7 Down game.
12. 🎲 **$supsdownguess [guess]** - Guess the sum in the 7 Up 7 Down game.
    Valid guesses: '7up', '7down', or '7'.
13. 🕹️ **$hangman** - Start the game Hangman.
14. 🤔 **$guess_letter [letter]** - Input the letter to be guessed using this command.
15. 💼 **$exithangman** - Quit hangman game. 
16. ℹ️ **$camelhelp** - Display this help message. Because even camel riders need directions sometimes.
17. 💰 **$deductmoney [user] [amount]** - Deduct camel coins from your balance. (Admin only)
"""
  await ctx.send(help_message)
  
@client.command()
async def guess_letter(ctx, letter: str):
  global game_instance_hangman
  global game_in_progress

  if not game_in_progress:
    await ctx.send("No Hangman game in progress.")
    return
  
  game_over, result_message = await game_instance_hangman.guess_letter(ctx, letter.lower())
  await ctx.send(result_message)
  
  if result_message.startswith("Suffocation"):
    await ctx.send(f"Prepare to suffer")
    limit = 1
    jokeurl = 'https://api.api-ninjas.com/v1/jokes?limit={}'.format(limit)
    response = requests.get(jokeurl, headers={'X-Api-Key': os.getenv("APININJAS") })
    if response.status_code == requests.codes.ok:
      await ctx.send(response.text[10:-2])
    else:
      await ctx.send("Error:", response.status_code, response.text)
      
  if game_over:
      game_in_progress = False
      await ctx.send("Type $restart_hangman to start a new game.")
    
@client.command()
async def restart_hangman(ctx):
    global game_instance_hangman
    global game_in_progress

    game_instance_hangman.reset_game()
    await game_instance_hangman.get_current_state(ctx)
    game_in_progress = True
  
@client.command()
async def exithangman(ctx):
    global game_instance_hangman
    game_instance_hangman = None  # Reset the game instance to exit Hangman
    await ctx.send("Winners never Quit. But you did, so you are not winner. Then who are you? Quitter? Twitter? Elon Musk?")

@client.command()
async def addmoney(ctx,target: discord.Member, coins: int):
  if ctx.message.author.id == int(os.environ['ADMIN_ID']):
    user_id = target.id
    if str(user_id) in db.keys():
      db[str(user_id)] += coins
    else:
      db[str(user_id)] = coins
    await ctx.send(f"Added {coins} camel coins:camel: to the balance.:white_check_mark:")
  else:
    await ctx.send("You are not authorized to use this command.:x:")

@client.command()
async def deductmoney(ctx,target: discord.Member, coins: int):
  if ctx.message.author.id == int(os.environ['ADMIN_ID']):
    user_id = target.id
    if str(user_id) in db.keys():
      db[str(user_id)] -= coins
    else:
      db[str(user_id)] = coins
    await ctx.send(f"Deducted {coins} camel coins:camel: from the balance.:white_check_mark:")
  else:
    await ctx.send("You are not authorized to use this command.:x:")

@client.command()
async def bet(ctx, coins: int):
  global game_in_progress
  global bet_amount
  user_id = ctx.message.author.id
  if (db[str(user_id)] < coins):
    await ctx.send("Looks like you're trying to gamble with sand instead of coins!:cactus::camel: Maybe it's time to find a treasure trove instead of scraping the dunes.")
  if (game_in_progress == False):
    bet_amount = coins
    add_money(user_id, -bet_amount)
    await ctx.send(f"You're putting {bet_amount} of your desert savings on the line!:camel::money_mouth: Let's hope it's not a mirage.")
  else:
    global channel_id
    general = client.get_channel(channel_id)
    await general.send(f"Hold your horses! A game's already underway. Patience, my friend.")
  
@client.command()
async def balance(ctx):
  user_id = ctx.message.author.id
  if (str(user_id) not in db.keys()):
    db[str(user_id)] = 100
  await ctx.send(f"Your treasure trove currently holds {db[str(user_id)]} camel coins!:camel::money_bag: Counting your camels before they hatch?")
                 
@client.command()
async def getbalance(ctx, target: discord.Member):
  user_id = target.id
  await ctx.send(f"Seems like {target.display_name} is counting their camel coins:camel: in the oasis... {db[str(user_id)]} found so far!:money_bag:")

def add_money(user_id, amount):
  db[str(user_id)] += amount

@client.command()
async def give(ctx, target: discord.Member, amount: int):
  giver_id = ctx.author.id
  target_id = target.id

  if giver_id == target_id:
    await ctx.send("Why are you trying to give yourself gifts? Feeling lonely, huh?:thinking:")
    return

  if amount <= 0:
    await ctx.send("You can't give negative or zero camel coins:camel:!")
    return

  if db[str(giver_id)] < amount:
    await ctx.send("Uh-oh! Looks like your generosity exceeds your wealth!:money_with_wings")
    return

  add_money(giver_id, -amount)
  add_money(target_id, amount)
  await ctx.send(f"{amount} camel coins have been humbly presented to {target.display_name}!:gift: Watch out for sandstorms, though.")

@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')

@client.command()
async def hello(ctx):
    await ctx.send("Well, well, well... Look who finally decided to emerge from their hobbit hole!:smirk::house: Welcome back to the land of the living, b*tch,")
  
@client.command()
async def steal(ctx, target: discord.Member, amount: int):
  thief_id = ctx.author.id
  target_id = target.id
  
  if thief_id == target_id:
    await ctx.send("Stealing from yourself? That's like trying to outsmart a mirror!:mirror: Maybe time to rethink your strategy, eh?")
    return

  if amount < 10:
    await ctx.send("Trying to pilfer less than ten camel coins:camel:? Looks like someone's aiming for petty theft! Aim higher, or at least aim for double digits!:man_shrugging:")
    return

  if amount > 100:
    await ctx.send("You can't be that greedy! Maximum steal limit is 100 camel coins:camel:.:smiling_imp:")
    return

  if db[str(thief_id)] < amount//2:
    await ctx.send("You don't have enough camel coins:camel: to attempt a steal!:smiling_face_with_tear:") 
    return
  
  if db[str(target_id)] < amount:
    await ctx.send("The target doesn't have enough camel coins:camel: to steal!:disappointed:")
    return

  success_probability = max(0.01, 0.7 - amount / 100)
  if random.random() < success_probability:
    db[str(thief_id)] += amount
    db[str(target_id)] -= amount

    await ctx.send(f"{ctx.author.mention} successfully stole {amount} camel coins:camel: from {target.mention}!:money_with_wings:")
  
  else:
    penalty_amount = amount // 2
    db[str(thief_id)] -= penalty_amount
    await ctx.send(f"{ctx.author.mention} attempted to steal {amount} camel coins from {target.mention}, but failed and incurred a penalty of {penalty_amount} camel coins:camel:!")
    
@client.command()
async def number(ctx):
  global game_in_progress
  if (game_in_progress):
    await ctx.send(f"A game is already in progress. Please wait for it to finish.")
    return
  await ctx.send("Welcome to the Number Guessing Game! I'm thinking of a number between 1 and 100. Try to guess it!")
  game_in_progress = True
  game_instance_number.reset_game()
  
@client.command()
async def numberguess(ctx, guess: int):
  global bet_amount
  global game_in_progress
  if (game_in_progress == False):
    await ctx.send("There's no game in progress. Start a new game with $number.")
    return
  result_message = game_instance_number.guess_number(guess)
  if discord.utils.get(ctx.author.roles, name="Red Role"):
    game_instance_number.attempts += 14
  await ctx.send(result_message)
  if result_message.startswith("Congratulations"):
    game_instance_number.reset_game()
    await ctx.send("Type $number to start a new game.")
    user_id = ctx.message.author.id
    add_money(user_id, 2*bet_amount)
    bet_amount = 0
    game_in_progress = False
  if result_message.startswith("You have used all your attempts"):
    game_instance_number.reset_game()
    bet_amount = 0
    game_in_progress = False
    await ctx.send("Type $number to start a new game.")

@client.command()
async def numberexit(ctx):
  global game_in_progress
  if (game_in_progress == False):
    await ctx.send("There's no game in progress right now. Let's get this party started!")
    return
  await ctx.send("Quitting already? Well, I guess the exit door is just the right size for your small ambitions.")
  game_in_progress = False
  await ctx.send("Type $number to start a new game.")

@client.command()
async def supsdown(ctx):
  global game_in_progress
  if (game_in_progress):
    await ctx.send(f"Hold your horses! A game's already underway. Patience, my friend.")
    return
  game_in_progress = True
  await ctx.send("Welcome to 7 Up 7 Down! :game_die: I'm rolling two dice. Guess whether it is 7up, 7down or 7?")

@client.command()
async def supsdownguess(ctx, guess: str):
  global bet_amount
  global game_instance_supsdown
  global game_in_progress
  if (game_in_progress == False):
    await ctx.send("No game in progress. Type $supsdown to start a new game.")
    return
  if (guess != "7up" and guess != "7down" and guess != "7"):
    await ctx.send("Invalid guess. Please enter either '7up', '7down', or '7'.")
    return
  result_message = game_instance_supsdown.roll(guess)
  await ctx.send(result_message)
  if result_message.startswith("Congratulations") and discord.utils.get(ctx.author.roles, name="Green Role"):
    user_id = ctx.message.author.id
    add_money(user_id, 3 * bet_amount)  # Triple the bet amount if they have the Green Role
    bet_amount = 0
    game_instance_supsdown.reset_game()
    game_in_progress = False
    await ctx.send("Type $supsdown to start a new game.")
  
  elif result_message.startswith("Congratulations"):
    if (guess == "7"):
      user_id = ctx.message.author.id
      add_money(user_id, 3*bet_amount)
    else:
      user_id = ctx.message.author.id
      add_money(user_id, 2*bet_amount)
    bet_amount = 0
    game_instance_supsdown.reset_game()
    game_in_progress = False
    await ctx.send("Type $supsdown to start a new game.")
  elif result_message.startswith("You have lost the bet"):
    game_instance_supsdown.reset_game()
    bet_amount = 0
    game_in_progress = False
    await ctx.send("Type $supsdown to start a new game.")

@client.command()
async def joke(ctx):
  limit = 1
  jokeurl = 'https://api.api-ninjas.com/v1/jokes?limit={}'.format(limit)
  response = requests.get(jokeurl, headers={'X-Api-Key': os.getenv("APININJAS") })
  if response.status_code == requests.codes.ok:
    await ctx.send(response.text[10:-2])
  else:
    await ctx.send("Error:", response.status_code, response.text)

@client.event
async def on_member_join(member):
  global channel_id
  general = client.get_channel(channel_id)
  await general.send(f"Welcome, {member.name}.:black_heart: Hope you brought your sense of humor and some camel coins:camel:. The void tends to demand both.:smiling_imp:")
  db[str(member.id)] = 100

@client.event
async def on_member_remove(member):
  user_id = member.id
  global channel_id
  general = client.get_channel(channel_id)
  del db[str(user_id)]
  await general.send(f"{member.name}, Nikal Lavde!")

def get_leaderboard(limit=5):
  user_balances = [(user_id, db[user_id]) for user_id in db.keys()]
  sorted_users = sorted(user_balances, key=lambda x: x[1], reverse=True)
  return sorted_users[:limit]

@client.command()
async def leaderboard(ctx):
  top_users = get_leaderboard()
  if top_users:
    leaderboard_message = "🏆 Leaderboard 🏆\n"
    for rank, (user_id, balance) in enumerate(top_users, start=1):
      user = client.get_user(int(user_id))
      if user:
        username = user.name
        leaderboard_message += f"{rank}. {username}: {balance} camel coins\n"
      else:
        leaderboard_message += f"{rank}. Unknown User: {balance} camel coins\n"
    await ctx.send(leaderboard_message)
  else:
    await ctx.send("The leaderboard is currently empty.")

store_items = {
    "1. Red Role": {
        "price": 20000,
        "role_name": "Red Role",  # Role name should match exactly with Discord role names
        "description": "Get 15 attempts in Number Guess Game (Red Colored Role)"
    },
    "2. Purple Role": {
        "price": 40000,
        "role_name": "Purple Role",
        "description": "For the love of purple. (Purple Colored Role)"
    },
    "3. Green Role": {
        "price": 60000,
        "role_name": "Green Role",
        "description": "Get triple the amount if guessed correctly in 7 Up and 7 Down (Green Colored Role)"
    },
    "4. Yellow Role": {
        "price": 70000000,
        "role_name": "Yellow Role",
        "description": "Saaath Kadod (Yellow Colored Role)"
    }
}



@client.command()
async def store(ctx):
    store_message = "🛒 **Welcome to the Store!** 🛒\n\nWrite $buy [number] to buy that specific role.\n\n"
    for item_name, item_details in store_items.items():
        description = item_details["description"]
        price = item_details["price"]
        store_message += f"**{item_name}**: {description}\nPrice: {price} camel coins\n\n"
    await ctx.send(store_message)

@client.command()
async def buy(ctx, item_number: int):
    user_id = str(ctx.author.id)
    if user_id not in db.keys():
        db[user_id] = 0

    # Check if the item number is valid
    if item_number < 1 or item_number > len(store_items):
        await ctx.send("Invalid item number.")
        return

    # Get the item details based on the item number
    item_keys = list(store_items.keys())
    item_name = item_keys[item_number - 1]  # Adjust index for 1-based numbering
    item_details = store_items[item_name]

    item_price = item_details["price"]
    if db[user_id] < item_price:
        await ctx.send("Insufficient balance to purchase this item.")
        return

    role_name = item_details["role_name"]
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        await ctx.send("Role not found. Please contact server admin.")
        return

    await ctx.author.add_roles(role)  # Assign role to user
    db[user_id] -= item_price  # Deduct coins from user's balance
    await ctx.send(f"Congratulations! You have purchased the {item_name}. Enjoy your new role.")


try:
    client.run(os.getenv("TOKEN"))
except Exception as err:
    raise err