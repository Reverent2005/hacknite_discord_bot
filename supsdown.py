import random
class updown:
  def __init__(self):
    self.dice1=random.randint(1,7)
    self.dice2=random.randint(1,7)
    
  def roll(self,guess):
    congrats =False
    
    if(self.dice1+self.dice2<7 and guess=="7down"):
      congrats = True
    elif(self.dice1+self.dice2>7 and guess=="7up"):
      congrats = True
    elif(self.dice1+self.dice2==7 and guess=="7"):
      congrats = True
    else:
      congrats = False
    if(congrats):
      return "Congratulations you won the bet "
    else:
      return "You have lost the bet"
  def reset_game(self):
    self.dice1=random.randint(1,7)
    self.dice2=random.randint(1,7)
    
    
    

