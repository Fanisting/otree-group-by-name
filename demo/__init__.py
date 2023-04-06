from otree.api import *


doc = """
App name: group_by_name
Author: Xuhang Fan, GitHub: https://github.com/Fanisting

Description: this app shows how to let participants to select their partner in a 2-agent group.

Pages:
1. Name: get each player's own name
2. Partner: get their expected partner's name
3. Wait: wait for all groups, prepare for group match
4. NotMatch: test whether some one is double-selected, if yes, the match should restart
5. MatchPage: group match here
6. Results: show the matching results

Note:
1. All of the nams are restricted, and should be found in the '_rooms/econ101.txt'
2. Designed for PLAYERS_PER_GROUP = 2, modify the code to make it more flexible
3. Now the group will be changed in every round, disable several pages to make the only for the first round 
4. According to the existing 'econ101.txt', the available names for test are: Alice, Bob, Claire, and Dana
5. Have fun!
"""


class C(BaseConstants):
    NAME_IN_URL = 'demo'
    PLAYERS_PER_GROUP = 2 # must be 2
    NUM_ROUNDS = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField(label = 'What is your name?')
    partner = models.StringField(label = 'Which partner do you want to match with? Insert the name.')
    identifier = models.IntegerField() # get every one's unique id for group match

# PAGES
class Name(Page):

    form_model = 'player'
    form_fields = ['name'] 

    # check the correctness of names here
    @staticmethod
    def error_message(player: Player, values):
        with open("_rooms/econ101.txt", "r") as file:
            names = file.read().splitlines()
        if (values['name'] in names) == False:
            return 'The name is invalid.'
        
class Partner(Page):

    form_model = 'player'
    form_fields = ['partner'] 

    # check the correctness of names here
    @staticmethod
    def error_message(player: Player, values):
        with open("_rooms/econ101.txt", "r") as file:
            names = file.read().splitlines()
        if (values['partner'] in names) == False:
            return 'The name is invalid.'
        if values['partner'] == player.name:
            return 'Do not insert your own name.'
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.identifier = player.participant.id_in_session
        
class NotMatch(Page):
    # if not match, show this page and end the game
    @staticmethod
    def is_displayed(player: Player):
        players = player.subsession.get_players()
        list = []
        for p in players:
            str = " ".join(sorted([p.name, p.partner]))
            temp =[str, p.identifier]
            list.append(temp)
        counts = {}
        for sublist in list:
            if sublist[0] in counts:
                counts[sublist[0]] += 1
            else:
                counts[sublist[0]] = 1
        match = True
        for value in counts.values():
            if value != 2:
                match = False
                break 
        print(match)
        return match == False
    
class Wait(WaitPage):
    wait_for_all_groups = True

class MatchPage(WaitPage):
    wait_for_all_groups = True
    # match here
    @staticmethod
    def after_all_players_arrive(subsession):
        players = subsession.get_players()
        list = []
        for p in players:
            str = " ".join(sorted([p.name, p.partner]))
            temp =[str, p.identifier]
            list.append(temp)
        import random
        random.shuffle(list)
        counts = {}
        for sublist in list:
            if sublist[0] in counts:
                counts[sublist[0]] += 1
            else:
                counts[sublist[0]] = 1
        print(counts)
        match = True
        for value in counts.values():
            if value != 2:
                match = False
                break
        indexs = {}
        if match == True:
            for sublist in list:
                if sublist[0] in indexs:
                    indexs[sublist[0]].append(sublist[1])
                else:
                    indexs[sublist[0]] = [sublist[1]]
        print(indexs)
        matrix = [value for value in indexs.values()]
        subsession.set_group_matrix(matrix)

class Results(Page):
    # show your group
    @staticmethod
    def vars_for_template(player: Player):
        other = player.get_others_in_group()[0].name
        return dict(other = other)
        
page_sequence = [Name, Partner, Wait, NotMatch, MatchPage, Results]
