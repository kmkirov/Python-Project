import player
import random


class building:

    def __init__(self, building_name,
                 color_street='a',
                 building_price=0,
                 perhouse_price=0,
                 buildig_fee_globa=0,
                 fee_with_one_house=0,
                 fee_with_two_house=0,
                 fee_with_three_house=0,
                 fee_with_four_house=0,
                 fee_with_five_house=0,
                 players_on_building=list(),
                 is_mourtaged=False,
                 owner=str(),
                 picture=None
                 ):

        self.building_name = building_name
        self.color_street = color_street  # neighborhood po dobre vunshen
        self.building_price = building_price
        self.perhouse_price = perhouse_price
        self.buildig_fee_globa = buildig_fee_globa

        self.fee_with_one_house = fee_with_one_house
        self.fee_with_two_house = fee_with_two_house
        self.fee_with_three_house = fee_with_three_house
        self.fee_with_four_house = fee_with_four_house
        self.fee_with_five_house = fee_with_five_house

        self.players_on_building = list()
        self.is_mourtaged = False
        self.owner = ' '

        self.picture = picture  # optional
        self.house_count = 0  # (4<= houses ,  5==hotel)!!!!!!!!
        self.with_house_fee = [self.buildig_fee_globa,
                               self.fee_with_one_house,
                               self.fee_with_two_house,
                               self.fee_with_three_house,
                               self.fee_with_four_house,
                               self.fee_with_five_house]

    def building_names(self):
        return self.building_name

    def mourtage(self, player):
        if self.owner == player and not self.is_mourtaged:
            player.add_money(self.building_price * 0.4)
            return True
        else:
            return False

    def unmourtage(self, player):
        if self.owner == player and not self.is_mourtaged:
            player.pay_money(self.building_price / 2)
            return True
        else:
            return False

    def get_color(self):
        return self.color_street

    def delete_player(self, player):
        if player in self.players_on_building:
            self.players_on_building.remove(player)

    def all_players(self):
        return self.players_on_building

    def buy_building(self, player, auctcion_buy=False):
        """
        check if the building have owner and current player have money to buy it
        auction mean that
        """
        # print(player)
        if self.owner == ' ' and (player.player_budget() >= self.building_price or auctcion_buy and auctcion_buy <= player.player_budget()):
            self.owner = player  # change ownar
            if auctcion_buy is False:
                # if he buyies it he is on it
                # self.players_on_building.append(player)#ne se polzva veche
                # player pays for the building
                player.pay_money(self.building_price)
                return True
            else:
                player.pay_money(auctcion_buy)
                return True
        return False

    def house_and_hotels_list(self):
        """
        return [house_count,hotel_count]
        if there is a hotel -> house_count=0
        """
        if self.house_count == 5:
            houses = 0
            hotel = 1
        else:
            houses = self.house_count
            hotel = 0
        return [houses, hotel]

    def bancrupt(self, player):  # bancrupt a player and add to owner
        # print(self.owner.get_items())
        """
        get the money + buildins from current player
        """
        if self.owner == ' ':
            return
        if player == self.owner:
            return
        for item in player.get_items():
            self.owner.get_items().append(item)
            item.change_owner(self.owner)

        self.owner.add_money(player.player_budget())  # take money
        player.add_items('bancrupt')
        # print(self.owner.get_items())

    def change_owner(self, player):  # on trade only
        if self.owner != ' ' and self.house_and_hotels_list() == [0, 0]:
            self.owner = player
            return True
        return False

    def take_fee(self, player, tax=0):
        """
          1) check if the building is owned from somebody -> if not can be bought
          2) if owned from current player didnt take fee

          3) tax if building is from that kind
          5) check for station fee and utility fee
          6) feee from normal building
          7) community or chance return it to game ....
        """
        print(self.owner,  self.color_street)
        # za krasota da pitam zashto ne raboti
        if self.owner == ' ' and self.color_street not in ['STATION', 'utility', 'CC', 'C', 'TAX']:
            return 'buy'
        # ako tova raboti shte rabotqt i ostanalite
        elif self.owner == player:  # totalno ne raboti
            return 'own'

        elif self.color_street == 'TAX':
            player.pay_money(self.with_house_fee[self.house_count])
            print(111)
            return 'TAX'

        elif self.color_street in ['STATION', 'utility']:
            if self.color_street == 'STATION':
                money = [25, 50, 100, 200]
                player.pay_money(money[self.owner.has_line('STATION')[1]])
                self.owner.add_money(money[count_stations])
                print(12)
                return 'STATION'
            else:
                a = random.randint(1, 7)
                b = random.randint(1, 7)
                money = [4, 10]
                player.pay_money(
                    (a + b) * money[self.owner.has_line('utility')[1]])
                self.owner.add_money((a + b) * money[count_stations])
                print(112)
                return 'utility'

        # tax:  # take fee from player
        elif not self.is_mourtaged and not self.owner == player and self.color_street not in ['CC', 'C']:
            player.pay_money(self.with_house_fee[self.house_count])
            self.owner.add_money(self.with_house_fee[self.house_count])
            # take money and return
            print(11)
            return 'fee'
        print(133)
        return self.color_street
        # elif self.color_street not in ['CC','C','TAX','JAIL','FREE']:
            # print(1)
            # return self.color_street

            # ne se polzva
    def have_owner(self):
        return self.owner

    def build_house(self, player):
        """
        if we have hotel it means 0 housesh 1 hotel
        if we dist
        """
        if not self.is_mourtaged and self.owner == player:
            if player.has_line(self.color_street)[0] and self.house_count < 5:
                self.house_count = self.house_count + 1
                player.pay_money(self.perhouse_price)
                return True
        return False

    def sell_house(self, player):
        """
        add money to player by formula price * 0.40
        """
        if not self.is_mourtaged and self.owner == player:
            if self.house_count > 0:
                self.house_count = self.house_count - 1
                player.add_money(self.perhouse_price * 0.40)
                return True
        return False

    def __str__(self):
        return self.building_name

    def __len__(self):
        return 1
    #    return self
    # def __iter__(self):
    #    return self.__next__()
