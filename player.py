import re
import random

DICT_OF_COLORS = {'Purple': 2, 'Light-Green': 3, 'Violet': 3, 'Orange': 3,
                  'Red': 3, 'Yellow': 3, 'Dark-Green': 3, 'Dark-Blue': 2,
                  'STATION': 0, 'TAX': 0}
JAIL_court = 30
JAIL = 10
FIELD = 39


class Player:

    def __init__(self, player_name, picture=None):
        self.player_name = player_name
        self.budget = 1500
        self.list_of_items = list()  # buildigns
        self.picture = picture
        self.in_jail = False
        self.list_cards = 0  # miss :)
        self.position = 0
        self.jail_cards = 0
    # da si napisha funkciqza jail_card in jail

    def player_budget(self):
        return self.budget

    def get_picture(self):
        return [self.picture, self.position]

    def playername(self):
        return self.player_name

    def add_money(self, money):
        self.budget = self.budget + money

    def pay_money(self, money):
        self.budget = self.budget - money

    def get_items(self):
        return self.list_of_items

    def jail(self):
        return self.in_jail

    def change_jail(self, status):
        self.in_jail = status

    def move_from_to(self, steps):
        """
        move player by steps and if he is on jail_court 30
        move him to jail 10  and change free variable
        """
        old_position = self.position
        self.position = (self.position + steps) % FIELD
        if self.position == JAIL_court:
            self.in_jail = 1
            self.position = JAIL
        return [old_position, self.position % FIELD]

    def has_line(self, color):
        """
        check if player has all buildings from color / build house
        """
        counter = 0
        for i in self.list_of_items:
            if re.search(color, i.get_color()):
                counter = counter + 1
        return [counter == DICT_OF_COLORS[color], counter]

    def house_and_hotels_counter(self):
        """
        count all hotels and houses in list of buildngs of the player
        ->[house,hotel]
        """
        house = 0
        hotel = 0
        for building in self.list_of_items:
            house, hotel = house + building.house_and_hotels_list()[
                0], hotel + building.house_and_hotels_list()[1]
        return [house, hotel]

    # def __str__(self):
    #    return self.player_name

    def add_items(self, items):
        """
        add building in the list
        """
        # test only
        if items == 'bancrupt':
            self.list_of_items = list()
        else:
            self.list_of_items.append(items)
