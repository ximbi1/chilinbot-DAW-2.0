class RealEstateGame:
    """Represents the Real Estate board game. Controls board creation, player
    creation, movement, Space purchasing, and game-state check. Communicates
    with
    Player class to move, purchase Spaces, and pay rent. Communicates with
    Space
    class to set ownership."""
    def __init__(self):
        """Initializes the Real Estate game with dictionaries to store
        players and
        game board spaces. Spaces dictionary is keyed with each Space's name
        with
        Space objects as values. Players dictionary is keyed with each
        Player's name
        with Player objects as values."""
        self._spaces: dict[str, Space] = {}
        self._players: dict[str, Player] = {}

    def create_spaces(self, go_money: int, rent_values: list):
        """Generates Space objects and 'GO' space. GO space generated uniquely,
        while Space objects are generated iteratively by the rent values list,
        one Space per value. Buy prices are generated depending on the rent
        values.
        Receives value of money awarded when passing GO and list of rent
        values."""
        self._spaces["GO"] = Space(None, go_money, None, 0)
        for rent_value, space_index in zip(rent_values,
                                           range(1,
                                                 len(rent_values) + 1)):
            # for space_index in range(1, len(rent_values) + 1):
            self._spaces[f"Space_{space_index}"] = Space(
                5 * rent_value, rent_value, None, space_index)

    def create_player(self, player_name: str, money_balance: int):
        """Creates a Player object and adds it to the "players" dictionary.
        Receives a
        name for the player and value of money awarded when passing GO."""
        spaces: dict[str, Space] = self.get_spaces()
        self._players[player_name]: Player = Player(
            self._spaces["GO"],
            money_balance,
            self._spaces["GO"].get_rent_value(),
            True,
            0,
            spaces,
            player_name,
        )

    def get_player_account_balance(self, player_name: str):
        """Returns input player's account balance by running Player's
        get_money_balance method. Receives player name to access "players"
        dictionary
        for Player object."""
        return self._players[player_name].get_money_balance()

    def get_player_current_position(self, player_name: str):
        """Returns input player's current position as integer by running
        Player's
        get_position method. Receives player name to access "players"
        dictionary for
        Player object."""
        return self._players[player_name].get_position()

    def get_players(self):
        """Returns the "players" dictionary."""
        return self._players

    def get_spaces(self):
        """Returns the "spaces" dictionary."""
        return self._spaces

    def buy_space(self, player_name: str):
        """Purchases the input player's current Space for that player. Uses
        Player's
        methods get_current_space and set_money_balance to get the Space
        object and
        adjust player's money. Uses Space's methods get_buy_value to get
        purchase
        price, get_position to make sure it's not the GO Space, get_owner to
        check if
        its owned already, and set_owner to set the Space's owner to the
        purchasing
        player. Uses RealEstateGame's get_player_account_balance to get
        player's
        balance. Receives player's name to access "players" dictionary for
        the Player
        object."""
        player: Player = self._players[player_name]
        player_balance: int = self.get_player_account_balance(player_name)
        space_to_buy: Space = player.get_current_space()
        buy_value: int = space_to_buy.get_buy_value()
        if space_to_buy.get_position() == 0:
            return False
        if player_balance > buy_value and space_to_buy.get_owner() is None:
            player.set_money_balance(-buy_value)
            space_to_buy.set_owner(player)
            return True
        else:
            return False

    def space_info(self, player_name: str):
        """Prints information about the player's current space."""
        player_space = self._players[player_name].get_current_space()
        try:
            owner = player_space.get_owner().get_name()
        except AttributeError:
            owner = "None"
        return {
            "position": player_space.get_position(),
            "owner": owner,
            "buy_value": player_space.get_buy_value(),
            "rent_value": player_space.get_rent_value(),
        }

    def move_player(self, player_name: str, move_spaces: int):
        """Moves player a certain number of spaces. Checks if player's
        balance > 0; if
        not, returns without action. Uses RealEstateGames'
        get_player_account_balance
        to get player's balance. Uses Player's methods set_position to handle
        moving, get_current_space to get the Space object the player moved
        to, and
        set_money_balance to adjust balances for rent. Uses Space's methods
        get_owner
        to get the Space's owner's Player object and get_rent_value to get
        rent price.
        Receives player's name to access "players" dictionary for Player
        object and
        integer number of spaces to move."""
        player: Player = self._players[player_name]
        if self.get_player_account_balance(player_name) <= 0:
            return
        player.set_position(move_spaces)
        new_space: Space = player.get_current_space()
        new_space_owner: Player = new_space.get_owner()
        if new_space_owner is None:
            return
        if new_space_owner is player:
            return
        new_space_rent: int = new_space.get_rent_value()
        new_space_owner.set_money_balance(
            player.set_money_balance(-new_space_rent))
        return

    def check_game_over(self):
        """Checks game state to see if it is finished. Iterates through
        "players"
        dictionary to check each player's status. Uses Player's methods
        get_status to
        get their status and get_name to get their name. Returns winner's name
        or empty string if game is still running."""
        active_players: int = 0
        winner = None
        for player in self._players.values():
            if player.get_status():
                active_players += 1
        if active_players == 1:
            for player in self._players.values():
                if player.get_status():
                    winner = player.get_name()
            return winner
        return ""


class Player:
    """Represents a player entity with current space, name, money balance,
    active status, board position, dictionary of board spaces, and GO award
    money
    attributes. Communicates with RealEstateGame class to move, purchase
    Spaces,
    pay rent, and set active status. Communicates with Space class to set
    ownership
    and pay rent."""
    def __init__(
        self,
        current_space,
        money_balance: int,
        go_money: int,
        active_player: bool,
        position: int,
        spaces,
        player_name: str,
    ):
        """Initializes a Player object with current space, GO award value,
        active status, name, dictionary of board spaces, and position
        parameters.
        Active status attribute is set by init."""
        self._current_space: Space = current_space
        self._money_balance: int = money_balance
        self._active_player: bool = active_player
        self._position: int = position
        self._go_money: int = go_money
        self._spaces: dict[str, Space] = spaces
        self._name: str = player_name

    def get_status(self):
        """Returns player's active status."""
        return self._active_player

    def get_name(self):
        """Returns the player's name."""
        return self._name

    def get_money_balance(self):
        """Returns the player's current account balance."""
        return self._money_balance

    def set_money_balance(self, value: int):
        """Adjusts the player's account balance and returns the absolute
        value of the
        amount adjusted. Cannot be adjusted below 0. Sets active status to
        False if
        balance goes to 0 and releases Space ownership."""
        self._money_balance += value
        if self._money_balance < 0:
            balance_difference: int = 0 - self._money_balance
            self._money_balance = 0
            self._active_player = False
            for space in self._spaces.values():
                if space.get_owner() == self:
                    space.set_owner(None)
            return balance_difference
        return abs(value)

    def get_position(self):
        """Returns the player's current position as an integer."""
        return self._position

    def set_position(self, move_spaces: int):
        """Increments player's current position by given integer amount and
        sets
        their current space to the Space object at that board index. Wraps back
        around GO space and adds GO money if player passes end of the board.
        Uses
        Player's methods get_position to get position and set_money_balance
        to award GO
        money. Uses Space's get_position to get board index."""
        current_position: int = self.get_position()
        new_position: int = current_position + move_spaces
        spaces: dict[str, Space] = self._spaces
        if new_position > 24:
            new_position -= 25
            self.set_money_balance(self._go_money)
        for space in spaces.values():
            if space.get_position() == new_position:
                self._current_space = space
                break
        self._position = new_position

    def get_current_space(self):
        """Returns the Space object the player is currently on."""
        return self._current_space


class Space:
    """Represents a board space object with position, buy and rent values,
    and owner
    attributes. Communicate with RealEstateGame class to set ownership and
    pay rent. Communicates with Player class to set ownership and pay rent."""
    def __init__(
        self,
        buy_value,
        rent_value: int,
        owner,
        position: int,
    ):
        """Initializes Space object with position, rent and buy values,
        and owner
        attributes."""
        self._buy_value: int = buy_value
        self._rent_value: int = rent_value
        self._owner: Player = owner
        self._position: int = position

    def get_buy_value(self):
        """Returns Space object's purchase price."""
        return self._buy_value

    def get_rent_value(self):
        """Returns Space object's rent price."""
        return self._rent_value

    def get_owner(self):
        """Returns the Space object's current owner as Player object."""
        return self._owner

    def set_owner(self, player):
        """Sets the Space's current owner to specified player."""
        self._owner = player

    def get_position(self):
        """Returns the Space objects position as an integer."""
        return self._position
