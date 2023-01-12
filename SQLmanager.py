import sqlite3

con = sqlite3.connect('data.db')

class db():
    def NewDatabase():
        cur = con.cursor()
        
        # Create table
        # TODO add unique guesses of green, yellow, white
        # win percent, average num of guesses
        try:
            cur.execute('''CREATE TABLE leaderboard (name text, wins real, score real)''')
        
            # Save (commit) the changes
            con.commit()
        except:
            print('table already exists')

    # deprec
    def GetLeaderboard():
        cur = con.cursor()
        rows = [('Name','Wins','Score')]
        for row in cur.execute("SELECT * FROM leaderboard ORDER BY wins"):
            rows.append(row)
        return rows

    def ShowLeaderboard():
        cur = con.cursor()
        rows = ['Name    |    Wins    |    Score']
        for row in cur.execute("SELECT * FROM leaderboard ORDER BY wins"):
            new_row = []
            for item in row:
                new_item = None
                try:
                    new_item = int(item)
                except:
                    new_item = item
                new_row.append(str(new_item))
            rows.append('    |    '.join(new_row))
        return '```'+'\n'.join(rows)+'```'
    
    def GetNames():
        cur = con.cursor()
        rows = []
        for row in cur.execute("SELECT name FROM leaderboard"):
            rows.append(row)
        return rows

    def NewUser(username):
        cur = con.cursor()
        arr = list(cur.execute("SELECT name FROM leaderboard WHERE name = (?)",(str(username),)))
        if len(arr) > 0:
            return 'User already exists'
        else:
            cur.execute("INSERT INTO leaderboard VALUES (?,?,?)",(str(username),0,0))
            con.commit()
            return 'User created'

    def SaveData(username):
        cur = con.cursor()

    def AddWin(username):
        cur = con.cursor()
        new_wins = 0
        try:
            arr = list(cur.execute("SELECT wins FROM leaderboard WHERE name = (?)",(str(username),)))
            new_wins = arr[0][0] + 1.0
            cur.execute("UPDATE leaderboard SET wins = (?) WHERE name = (?)",(new_wins,str(username)))
            con.commit()
            return 'Win added'
        except:
            arr = list(cur.execute("SELECT name FROM leaderboard WHERE name = (?)",(str(username),)))
            if len(arr) > 0:
                return 'User already exists'
            else:
                cur.execute("INSERT INTO leaderboard VALUES (?,?,?)",(str(username),0,0))
                con.commit()
                return 'User created'

db.NewDatabase()