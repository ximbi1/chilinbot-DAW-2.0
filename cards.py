import requests
import json

def deck():
  deck = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1").json()
  return deck["deck_id"]

def draw(deck, count = 1):
  #JSON decoder randomly fails. This is the only way i found to fix it
  error = True
  while error:
    try:
      drawed_raw = requests.get(f"https://deckofcardsapi.com/api/deck/{deck}/draw/?count={count}").json()
      error = False
    except json.decoder.JSONDecodeError:
      error = True
  cards = []
  for card in range(count):
    cards.append(drawed_raw["cards"][card]["code"])
  
  return cards
  
def values(deck, pile):
  values = requests.get(f"https://deckofcardsapi.com/api/deck/{deck}/pile/{pile}/list/").json()
  returner = []
  for card in values["piles"][pile]["cards"]:    
    returner.append(card["value"])
  return returner

def codes(deck, pile):
  codes = requests.get(f"https://deckofcardsapi.com/api/deck/{deck}/pile/{pile}/list/").json()
  returner = []
  for card in codes["piles"][pile]["cards"]:    
    returner.append(card["code"])
  return returner

def add_pile(deck, pile, cards):
  if type(cards) is not str:
    cardS = ""
    for card in cards:
      cardS = cardS + card + ","
  else:
    cardS = cards
  requests.get(f"https://deckofcardsapi.com/api/deck/{deck}/pile/{pile}/add/?cards={cardS}").json()

  return codes(deck, pile)

def value(deck, pile):
  total = 0
  aces = 0
  for card in values(deck, pile):
    try:
      card = int(card)
    except Exception:
      if card != "ACE":
        card = 10
      else:
        aces += 1
        card = 0
    total += card
    
  for i in range(aces):
    if total <= (11 - aces):
      total += 11
    else:
      total += 1
  return total

def pile(deck, pile):
  returner = ""
  for card in codes(deck, pile):
    if card != codes(deck, pile)[-1]:
      card = card + ", " 
    card = card.replace("0", "10")
    card = card.replace("C", "♠")
    card = card.replace("H", "♥")
    card = card.replace("S", "♣️")
    card = card.replace("D", "♦️")
    returner = returner + card     
  
  return returner