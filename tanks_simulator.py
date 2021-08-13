#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 11:49:53 2021

@author: MME
"""

# Lets simulate The Tanks

# Tanks got 3 HP
# Tanks can shoot 3 block away
# Tanks can either move or shoot or save an action for later

import random
import numpy as np
import scipy
import sys


def generate_color():
    color_list = ['azure',
                  'black',
                  'blue',
                  'brown',
                  'cyan',
                  'gold',
                  'grey',
                  'green',
                  'indianred',
                  'indigo',
                  'ivory',
                  'lime',
                  'magenta',
                  'orange',
                  'pink',
                  'purple',
                  'red',
                  'silver',
                  'violet',
                  'white',
                  'yellow'
                  ]
    return random.choice(color_list)


def generate_name():
    # https://www.englishclub.com/vocabulary/animal-terms-easy.htm
    animal_list = ['ants',
                   'birds',
                   'cats',
                   'chickens',
                   'cows',
                   'dogs',
                   'elephants',
                   'fishes',
                   'foxes',
                   'horses',
                   'kangaroos',
                   'lions',
                   'penguins',
                   'rabbits',
                   'sheep',
                   'tigers',
                   'whales',
                   'wolves'
                   ]
    return random.choice(animal_list)


class tank():
    def __init__(self,
                 pos_x,
                 pos_y,
                 life=3,
                 action_value=1,
                 direction=random.choice(["N", "S", "E", "W"]),
                 move_cost=1,
                 shoot_cost=1,
                 shoot_dmg=1,
                 shoot_range=2,
                 color="blue",
                 team="Blue Hedgehogs",
                 animal="hedgehogs",
                 nb_id=0,
                 char=">"
                 ):

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.life = life
        self.action_value = action_value
        self.direction = direction
        self.dir_char_dict = {"N": "∧",
                              "S": "v",
                              "E": ">",
                              "W": "<"}
        self.dir_char = self.dir_char_dict[direction]
        self.movement_dict = {"N": (0, 1),
                              "S": (0, -1),
                              "E": (1, 0),
                              "W": (-1, 0)}
        self.shoot_cost = shoot_cost
        self.shoot_dmg = shoot_dmg
        self.shoot_range = shoot_range
        self.move_cost = move_cost
        self.color = color
        self.team = team
        self.animal = animal
        self.id = str(nb_id)

        self.char = char

    def move(self, direction):
        self.action_value -= self.move_cost
        vector_x, vector_y = self.movement_dict[direction]
        self.pos_x += vector_x
        self.pos_y += vector_y
        self.update_dir_char(direction)

    def update_dir_char(self, direction):
        self.dir_char = self.dir_char_dict[direction]

    def shoot(self):
        self.action_value -= self.shoot_cost

    def save_action(self):
        pass

    def change_direction(self, new_dir):
        self.direction = new_dir

    def get_action_list(self):
        action_list = ["save_action"]
        if (self.action_value - self.shoot_cost) >= 0:
            action_list.append("shoot")
        if (self.action_value - self.move_cost) >= 0:
            action_list.append("move")

        return action_list

    def get_team_name(self):
        return self.color.capitalize() + " " + self.team.capitalize()


class battlefield():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.board = [["_" for x in range(j)] for y in range(i)]
        self.tank_list = {}

    def get_occupied_position(self):
        list_pos = []
        for x in range(self.i):
            for y in range(self.j):
                if self.board[x][y] != 0:
                    list_pos.append((x, y))
        return list_pos

    def get_free_pos(self):
        if self.tank_list == {}:
            return random.randint(0, self.i - 1), random.randint(0, self.j - 1)
        else:
            occupied_pos = []
            for team in self.tank_list.keys():
                for tank in self.tank_list[team]:
                    occupied_pos.append((tank.pos_x, tank.pos_y))
            x = random.randint(0, self.i - 1)
            y = random.randint(0, self.j - 1)
            while (x, y) in occupied_pos:
                x = random.randint(0, self.i - 1)
                y = random.randint(0, self.j - 1)
            return x, y

    def generate_tank(self,
                      pos_x,
                      pos_y,
                      color,
                      team,
                      animal,
                      id_nb,
                      char="<"):
        self.tank_list[team].append(tank(pos_x,
                                         pos_y,
                                         color=color,
                                         team=team,
                                         animal=animal,
                                         nb_id=id_nb,
                                         char=char))

    def get_team_name(self):
        color = generate_color()
        animal = generate_name()
        team = color.capitalize() + " " + animal.capitalize()
        while team in self.tank_list.keys():
            color = generate_color()
            animal = generate_name()
            team = color.capitalize() + " " + animal.capitalize()
        return team, color, animal

    def generate_team(self, nb_tank, char=">"):
        team, color, animal = self.get_team_name()
        self.tank_list[team] = []

        for i in range(nb_tank):
            pos_x, pos_y = self.get_free_pos()
            self.generate_tank(pos_x,
                               pos_y,
                               color,
                               team,
                               animal,
                               i + 1,
                               char=char
                               )
            self.board[pos_x][pos_y] = char  # ">"
            i += 1

    def generate_default_battle(self):
        self.generate_team(2, char="Ω")
        self.generate_team(2, char="α")
        self.update_board()
        self.show_board()

    def update_board(self):
        if len(self.tank_list.keys()) == 1:
            print(list(self.tank_list.keys())[0] + " is the winner!!!")
            return "Victory"

        new_board = [["_" for x in range(self.j)] for y in range(self.i)]
        for team in self.tank_list.keys():
            for tank in self.tank_list[team]:
                # color = tank.color
                new_board[tank.pos_x][tank.pos_y] = str(tank.life)  # tank.char  # tank.dir_char
        self.board = new_board

    def show_board(self):
        for team in self.tank_list.keys():
            print(team + " " + str(len(self.tank_list[team])))
            # print(" ".join([str((tank.id, str(tank.life), str(tank.pos_x), str(tank.pos_y))) for tank in self.tank_list[team]]))
        for row in self.board[::-1]:
            print(" ".join(row))
        print("")

    def battle_turn(self):
        """
        For each tank parse round.
        """
        for team in sorted(self.tank_list.keys()):
            for tank in self.tank_list[team]:
                tank.action_value += 1
                self.do_tank_action(tank)
                if self.update_board():
                    return "Victory"
                self.show_board()

    def do_tank_action(self, tank):
        action_list = tank.get_action_list()
        closest_enemy, dist = self.get_closest_enemy_tank(tank)

        if "shoot" in action_list and dist <= tank.shoot_range:
            print(tank.team + " " + tank.id + " shoot")
            self.resolve_shooting(tank, closest_enemy)
        elif "move" in action_list:
            print(tank.team + " " + tank.id + " move")
            # get direction toward enemy
            direction = self.get_to_closest((tank.pos_x, tank.pos_y),
                                            (closest_enemy.pos_x, closest_enemy.pos_y))
            tank.move(direction)

    def get_to_closest(self, pos1, pos2):
        """
        return the direction which get pos1 the closest to pos2
        """
        direction = ["N", "S", "E", "W"]
        values = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        new_pos = [(pos1[0] + val[0], pos1[1] + val[1]) for val in values]
        dist = scipy.spatial.distance.cdist([pos2], new_pos)
        i = dist.argmin()
        return direction[i]

    def get_closest_enemy_tank(self, tank):
        enemy_tank = []
        l_enemy_team = list(self.tank_list.keys())
        l_enemy_team.remove(tank.team)

        for team in l_enemy_team:
            enemy_tank += self.tank_list[team]

        enemy_tank_pos_list = np.array([(t.pos_x, t.pos_y) for t in enemy_tank])
        tank_pos = np.array([(tank.pos_x, tank.pos_y)])
        dist = scipy.spatial.distance.cdist(tank_pos, enemy_tank_pos_list)
        i = dist.argmin()
        closest_enemy = enemy_tank[i]
        return closest_enemy, dist[0][i]

    def resolve_shooting(self, t1, t2):
        t2.life -= t1.shoot_dmg
        if t2.life <= 0:
            self.tank_list[t2.team].remove(t2)
            if self.tank_list[t2.team] == []:
                self.tank_list.pop(t2.team)

    def solve_battle(self):
        print(self.board)


if __name__ == "__main__":
    battle = battlefield(7, 7)
    battle.generate_default_battle()
    battle.battle_turn()
