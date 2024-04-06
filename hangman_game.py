import random
import os
import discord
import asyncio


def get_word_list():
  word_list = [
      "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua",
      "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas",
      "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize",
      "Benin", "Bhutan", "Bolivia", "Bosnia", "Botswana", "Brazil", "Brunei",
      "Bulgaria", "Burkina", "Burundi", "Cabo", "Cambodia", "Cameroon",
      "Canada", "Central", "Chad", "Chile", "China", "Colombia", "Comoros",
      "Congo", "Costa", "Croatia", "Cuba", "Cyprus", "Czech", "Denmark",
      "Djibouti", "Dominica", "Dominican", "Ecuador", "Egypt", "El",
      "Equatorial", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji",
      "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana",
      "Greece", "Grenada", "Guatemala", "Guinea", "Guyana", "Haiti",
      "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq",
      "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan",
      "Kenya", "Kiribati", "Korea", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos",
      "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
      "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia",
      "Maldives", "Mali", "Malta", "Marshall", "Mauritania", "Mauritius",
      "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro",
      "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal",
      "Netherlands", "Nicaragua", "Niger", "Nigeria", "North", "Norway",
      "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua", "Paraguay",
      "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania",
      "Russia", "Rwanda", "Saint", "Samoa", "San", "Sao", "Saudi", "Senegal",
      "Serbia", "Seychelles", "Sierra", "Singapore", "Slovakia", "Slovenia",
      "Solomon", "Somalia", "Spain", "America", "Sudan", "Suriname", "Sweden",
      "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand",
      "Timor-Leste", "Togo", "Tonga", "Trinidad", "Tunisia", "Turkey",
      "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United", "Uruguay",
      "Uzbekistan", "Vanuatu", "Vatican", "Venezuela", "Vietnam", "Yemen",
      "Zambia", "Zimbabwe"
  ]
  return word_list


class HangmanGame:

  def __init__(self, word_list, image_folder_path):
    self.word_list = word_list
    self.max_attempts = 5
    self.attempts_left = self.max_attempts
    self.reset_game()
    self.image_folder_path = image_folder_path
    self.first_time = True

  def reset_game(self):
    self.attempts_left = self.max_attempts
    self.current_word = random.choice(self.word_list).lower()
    self.guesses = set()
    self.masked_word = [
        '_' if char.isalpha() else char for char in self.current_word
    ]
    self.current_drawing_index = 0

  async def guess_letter(self, ctx, letter):
    letter = letter.lower()
    if letter in self.guesses:
      return False, "You've already guessed that letter!"

    self.guesses.add(letter)
    if letter in self.current_word:
      for i, char in enumerate(self.current_word):
        if char == letter:
          self.masked_word[i] = letter
      if '_' not in self.masked_word:
        return True, "Congratulations! You guessed the word: " + self.current_word
    else:
      self.attempts_left -= 1
      if self.attempts_left >= 0:
        self.current_drawing_index += 1
      if self.attempts_left == 0:
        return True, f"Suffocation killed the man:skull_crossbones:. The country was: " + self.current_word
    
    result_message = await self.get_current_state(ctx)
    if result_message.strip():  # Check if the message is not empty or whitespace
        await ctx.send(result_message)
    return False, result_message
    
  async def get_current_state(self, ctx):
    masked_word_display = ' '.join(self.masked_word)
    instructions = ""
    if self.first_time:
      instructions += (
          f"- Welcome to Hangman. The man must not hang, otherwise a bad joke is on its way to ruin your life.\n"
          f"- Number of letters in the word: {len(self.current_word)}\n")
      self.first_time = False
    instructions += (f"- Attempts left: {self.attempts_left}\n"
                     f"- Current word: {masked_word_display}\n"
                     f"- Hangman status:\n")
    if self.first_time:
      instructions += "- Start by guessing a letter using $guess_letter <letter>"
    else:
      instructions += "- Continue by guessing a letter using $guess_letter <letter>"
  
    if self.attempts_left == 0:
      self.current_drawing_index = 5
    image_path = f"images/{self.current_drawing_index}.jpg"
    instructions += "\nHere's the Hangman image:"
    await send_hangman_image(ctx, self, instructions)

  def get_current_drawing(self):
    image_filename = f"{self.current_drawing_index + 1}.jpg"
    image_path = os.path.join(self.image_folder_path, image_filename)
    return image_path


async def send_hangman_image(ctx, game_instance, message):
  image_path = game_instance.get_current_drawing()
  with open(image_path, "rb") as image_file:
    await ctx.send(content=message,
                   file=discord.File(image_file, "hangman_image.jpg"))
    # Introduce a delay after sending each message
    await asyncio.sleep(10)  # Adjust the delay time as needed
