###########WORDLE####################

alpha = list('abcdefghijklmnopqrstuvwxyz')

emojiID = { # do not touch !! (emoji ID)
  'a1':'957821979895947284',
  'b1':'957823925851680828',
  'c1':'957823925864263680',
  'd1':'957823926061396068',
  'e1':'957823925864255518',
  'f1':'957823926216564767',
  'g1':'957823926111703041',
  'h1':'957823926006874153',
  'i1':'957823926216556554',
  'j1':'957823925876834315',
  'k1':'957823926178820117',
  'l1':'957823925948153886',
  'm1':'957823926027829278',
  'n1':'957823926224957440',
  'o1':'957823926187216936',
  'p1':'957823926283694130',
  'q1':'957823926296256563',
  'r1':'957823926807973949',
  's1':'957823926329819146',
  't1':'957823926254317659',
  'u1':'957823926682132520',
  'v1':'957823926426284044',
  'w1':'957823927315476480',
  'x1':'957823926724087828',
  'y1':'957823926749237268',
  'z1':'957823926673752144',

  'a2':'958149639129923644',
  'b2':'958149639167676417',
  'c2':'958149638752436235',
  'd2':'958149639113150486',
  'e2':'958149639096397906',
  'f2':'958149639205433364',
  'g2':'958149639197061120',
  'h2':'958149639222226994',
  'i2':'958149639209623622',
  'j2':'958149639087992964',
  'k2':'958149639377416292',
  'l2':'958149638920237117',
  'm2':'958149639322877972',
  'n2':'958149639255781376',
  'o2':'958149639792648262',
  'p2':'958149639285133312',
  'q2':'958149639364821012',
  'r2':'958149639327059988',
  's2':'958149639540989982',
  't2':'958149639427727481',
  'u2':'958149639687794710',
  'v2':'958149639431933972',
  'w2':'958149639469674506',
  'x2':'958149639289339967',
  'y2':'958167806640271410',
  'z2':'958167806745133056',

  'a3':'957860591802920960',
  'b3':'957862672257388585',
  'c3':'957860591773577266',
  'd3':'957862672236433448',
  'e3':'957860591819698246',
  'f3':'957860591786156076',
  'g3':'957862672240619560',
  'h3':'957860591555477535',
  'i3':'957862672232230922',
  'j3':'957860591828090940',
  'k3':'957860591781965865',
  'l3':'957860591719047209',
  'm3':'957862672307720222',
  'n3':'957862672307720282',
  'o3':'957860591760990250',
  'p3':'957860591823900696',
  'q3':'957862672404189234',
  'r3':'957860591844851713',
  's3':'957862672395800586',
  't3':'958150066722447362',
  'u3':'958150030190067792',
  'v3':'957862672483893248',
  'w3':'958150390518530128',
  'x3':'958150412949663754',
  'y3':'958149717999624242',
  'z3':'958149717852827660'
}

def format_text(text, color):
  return ' '.join([f'<:wordle{char}{color}:{emojiID[char+color]}>' for char in text])

def generate(code):
  return ''.join([str(alpha.index(char)+9) for char in code])

def decode(code):
  i = 0
  l = []
  for c in range(int(len(code) / 2)):
    l.append(alpha[int(code[i:i + 2]) - 9])
    i += 2
  return (''.join(l))

def getwordletoday():
  t = str(date.today()).replace('-',' ').split()
  start = date(2022,2,22)
  today = date(int(t[0]),int(t[1]),int(t[2]))
  file = open('wordlist.txt','r').read().split()
  num = file.index('thorn')

  return file[num+(today-start).days+1]

def create_game(a, secret):
  activegames[hash(a)] = {}
  activegames[hash(a)]['game'] = [[],[],[],[],[],[]]
  activegames[hash(a)]['guessed'] = ['','','','','','']
  activegames[hash(a)]['secretword'] = secret
  activegames[hash(a)]['position'] = ['-' for i in range(5)]
  activegames[hash(a)]['correct'] = []
  activegames[hash(a)]['incorrect'] = []
  activegames[hash(a)]['turn'] = 0

def print_game(user):
  lines = []
  for line in activegames[user]['game']:
    if line:
      lines.append(line)
    else: lines.append('<:wordleblank:958171351615680623> '*5)
  return '\n'.join(lines)



@bot.event
async def on_message(message):
    m = message.content
    a = message.author
    if m == 'help':
      text = '''
      ```
-wordle: starts a new random game of wordle
-wordle today: starts a game of today's wordle
-end: ends your current game of wordle
-guess (word): places a guess on your current game of wordle
-active: checks if you have an active game
-position: view of your correctly positioned words
-correct: view your correct words but in an incorrect position
-incorrect: view your incorrectly guessed words
-giveup: show secret word
-game: bot re-sends your game
-info: gives information about the bot and Wordle
-create (word): creates a custom game of wordle for a friend
-custom (code): runs a custom game of wordle
-help: list of commands```
      '''
      await message.channel.send(text)

    # create game
    if m == 'a wordle':
      if not (hash(a) in activegames):
        create_game(a, secret=random.choice(open('wordlist.txt','r').read().split('\n')))
        await message.channel.send(print_game(hash(a)))
      else:
        await message.channel.send('You already have an active game! Use "!end" to end your game.')

    # create wordle today game
    if m == 'a wordle today':
      if not(hash(a) in activegames):
        create_game(a, secret=getwordletoday())
        await message.channel.send(print_game(hash(a)))
      else:
        await message.channel.send('You already have an active game! Use "!end" to end your game.')

    # custom game
    if m.split()[0] == 'a custom':
      code = m.split()[1]
      words = open('wordlist.txt','r').read().split('\n')
      try:
        if decode(code) in words:
          create_game(a, secret=decode(code))
          await message.channel.send(print_game(hash(a)))
        else: await message.channel.send('Invalid code.')
      except ValueError: await message.channel.send('Invalid code.')

    # destroy game
    if m == 'a end':
      if hash(a) in activegames:
        del activegames[hash(a)]
        await message.channel.send('Succesfully ended your game.')
      else:
        await message.channel.send('You do not currently have an active game! Use "!wordle" to start a new game.')

    # gives answer
    if m == 'a giveup':
      await message.channel.send(f'The word is {activegames[hash(a)]["secretword"]}')

    # reprints game
    if m == 'a game':
      if hash(a) in activegames:
        await message.channel.send(print_game(hash(a)))
      else:
        await message.channel.send('You do not have an active game.')

    # sends information
    if m == 'a info':
      embed = discord.Embed()
      embed.title = format_text('info', color='1')
      embed.description = 'Guess the **WORDLE** in six tries. ' \
                          '\nEach guess must be a valid five-letter word. ' \
                          '\nHit the enter button to submit. After each guess, the color of the tiles will change to show how close your guess was to the word. ' \
                          '\n\nUse !help for commands. ' 
      embed.color = 0x00b81f
      await message.channel.send(embed=embed)

    # creates custom game
    if m.split()[0] == 'a create':
      word = m.split()[1]
      if word in open('wordlist.txt','r').read().split('\n'):
        code = generate(list(word))
        await message.delete()
        await message.channel.send(f'Your custom game code is: {code}. Use "!custom {code}" to play the game.')
      else:
        await message.channel.send(f'"{word}" not in word list!')

    # checks for active games
    if m == 'a active':
      if hash(a) in activegames:
        await message.channel.send('You have an active game.')
      else: await message.channel.send('You do not have an active game.')

    # checks position
    if m == 'a position':
      try: await message.channel.send('```'+' '.join(activegames[hash(a)]['position'])+'```')
      except KeyError: await message.channel.send('You do not have an active game.')

    # checks correct
    if m == 'a correct':
      try:
        if not activegames[hash(a)]['correct']:
          await message.channel.send('```None.```')
        else:
          await message.channel.send('```'+', '.join(activegames[hash(a)]['correct'])+'```')
      except KeyError: await message.channel.send('You do not have an active game.')

    # checks incorrect
    if m == 'a incorrect':
      try:
        if not activegames[hash(a)]['incorrect']:
          await message.channel.send('```None.```')
        else:
          await message.channel.send(f'```'+', '.join(activegames[hash(a)]['incorrect'])+'```')
      except KeyError: await message.channel.send('You do not have an active game.')

    # guess
    if m.split()[0] == 'guess':
      if hash(a) in activegames:
        current_guess = m.split()[1]
        if current_guess == activegames[hash(a)]['secretword']:
          turn = activegames[hash(a)]['turn']
          final = [f'<:wordle{char}1:{emojiID[char+"1"]}>' for char in current_guess]
          activegames[hash(a)]['game'][turn] = ' '.join(final)
          await message.channel.send(print_game(hash(a)))
          await message.channel.send('You win!')
          del activegames[hash(a)]
        else:
          if current_guess in open('wordlist.txt','r').read().split('\n'):
            secretword = activegames[hash(a)]['secretword']
            position = activegames[hash(a)]['position']
            correct = activegames[hash(a)]['correct']
            incorrect = activegames[hash(a)]['incorrect']
            turn = activegames[hash(a)]['turn']
            final = ['-','-','-','-','-']

            for index, char in enumerate(current_guess):
              if current_guess[index] == secretword[index]:
                position[index] = char if not char in position else print()
                final[index] = f'<:wordle{char}1:{emojiID[char + "1"]}>'
              elif current_guess[index] in secretword:
                correct.append(char) if not char in correct else print()
                final[index] = f'<:wordle{char}2:{emojiID[char + "2"]}>'
              else:
                incorrect.append(char) if not char in incorrect else print()
                final[index] = f'<:wordle{char}3:{emojiID[char + "3"]}>'

            activegames[hash(a)]['game'][turn] = ' '.join(final)
            activegames[hash(a)]['position'] = position
            activegames[hash(a)]['correct'] = correct
            activegames[hash(a)]['incorrect'] = incorrect
            activegames[hash(a)]['guessed'][turn] = current_guess
            await message.channel.send(print_game(hash(a)))
            if turn == 5:
              del activegames[hash(a)]
              await message.channel.send(f'You lose! The word was: {secretword}!')
            else:
              activegames[hash(a)]['turn'] += 1
          else: await message.channel.send(f'"{current_guess}" not in word list!')
      else: await message.channel.send('You do not have an active game.')



############final wordle##########################