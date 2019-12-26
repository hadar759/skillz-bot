from base_bot import BaseBot
from penguin_game import *

if not __debug__:
    from typing import Union, List


class GenericBot(BaseBot):
    def do_turn(self):
        pass

    def attack(self):
        enemy_icebergs = self.game.get_enemy_icebergs()
        self.bubble_sort_by_peng(enemy_icebergs)
        for my_iceberg in self.game.get_my_icebergs():
            pass # TODO create attack with multiple attackers whenever i have time

    def iceberg_in_danger(self, iceberg):
        # type: (Iceberg) -> bool
        in_my_control = iceberg.owner == self.game.get_myself()
        friendly_headed = self.all_friendly_directed(iceberg)
        self.bubble_sort_by_distance(friendly_headed, iceberg)
        enemy_headed = self.all_enemy_directed(iceberg)
        self.bubble_sort_by_distance(enemy_headed, iceberg)
        friendly_index = 0
        enemy_index = 0
        cur_turns = 0
        cur_penguins = iceberg.penguin_amount

        for i in range(len(friendly_headed) + len(enemy_headed)):
            cur_friendly = friendly_headed[friendly_index]
            cur_enemy = enemy_headed[enemy_index]
            turns_till_friendly_arrival = cur_friendly.turns_till_arrival(iceberg)
            turns_till_enemy_arrival = cur_enemy.turns_till_arrival(iceberg)

            if turns_till_friendly_arrival < turns_till_enemy_arrival:
                if in_my_control:
                    cur_penguins += cur_friendly.penguin_amount \
                                    + iceberg.penguins_per_turn * (turns_till_friendly_arrival - cur_turns)
                else:
                    cur_penguins += - cur_friendly.penguin_amount \
                                    + iceberg.penguins_per_turn * (turns_till_friendly_arrival - cur_turns)
                friendly_index += 1
            else:
                if in_my_control:
                    cur_penguins += - cur_enemy.penguin_amount \
                                    + iceberg.penguins_per_turn * (turns_till_enemy_arrival - cur_turns)
                else:
                    cur_penguins += cur_enemy.penguin_amount \
                                    + iceberg.penguins_per_turn * (turns_till_enemy_arrival - cur_turns)
                enemy_index += 1

            if cur_penguins < 0:
                in_my_control = not in_my_control
                cur_penguins = - cur_penguins

        return not in_my_control

    def get_closest_iceberg_under_attack(self, my_iceberg):
        # type: (Iceberg) -> Union[Iceberg, None]
        """Returns the closest iceberg in danger"""
        friendly_icebergs = self.game.get_my_penguin_groups().remove(my_iceberg)
        self.bubble_sort_by_distance(friendly_icebergs, my_iceberg)

        for iceberg in friendly_icebergs:
            if self.iceberg_in_danger(iceberg):
                return iceberg

    def all_enemy_directed(self, destination):
        # type: (Iceberg) -> List[PenguinGroup]
        """Returns all enemy groups directed at the iceberg"""
        all_hostile = []
        for group in self.game.get_enemy_penguin_groups():
            if group.destination == destination:
                all_hostile.append(group)
        return all_hostile

    def total_enemy_peng_directed(self, destination):
        # type: (Iceberg) -> int
        """Returns the total number of friendly penguins directed at an iceberg"""
        total_enemy_directed = 0
        enemy_directed = self.all_enemy_directed(destination)
        for group in enemy_directed:
            total_enemy_directed += group.penguin_amount

        return total_enemy_directed

    def all_friendly_directed(self, destination):
        # type: (Iceberg) -> List[PenguinGroup]
        """Returns all friendly groups directed at the iceberg"""
        all_friendlies = []
        for group in self.game.get_my_penguin_groups():
            if group.destination == destination:
                all_friendlies.append(group)
        return all_friendlies

    def total_friendly_peng_directed(self, destination):
        # type: (Iceberg) -> int
        """Returns the total number of friendly penguins directed at an iceberg"""
        total_friendly_directed = 0
        friendly_directed = self.all_friendly_directed(destination)
        for group in friendly_directed:
            total_friendly_directed += group.penguin_amount

        return total_friendly_directed

    def get_peng_directed(self, iceberg):
        # type: (Iceberg) -> int
        """Returns the total number of penguins directed at an iceberg"""
        total_friendly = self.total_friendly_peng_directed(iceberg)
        total_enemy = self.total_enemy_peng_directed(iceberg)

        return total_friendly - total_enemy

    def calculate_num_of_peng(self, destination, origin):
        # type: (Iceberg, Iceberg) -> int
        """Calculates the total number of peng in a destination, by the time peng from origin arrive"""
        distance = origin.get_turns_till_arrival(destination)
        # Get the amount of friendly penguins directed to the iceberg
        my_peng_headed = self.total_friendly_peng_directed(destination)
        # Get the amount of enemy penguins directed to the iceberg
        enemy_peng_headed = self.total_enemy_peng_directed(destination)
        # If it's friendly we want to subtract the enemy penguins
        if destination in self.game.get_my_icebergs():
            enemy_peng_headed = - enemy_peng_headed
        # If it's an enemy we want to subtract the friendly penguins
        elif destination in self.game.get_enemy_icebergs():
            my_peng_headed = - my_peng_headed

        else:
            distance = 0

        return (destination.penguin_amount + destination.penguins_per_turn * distance +
                my_peng_headed + enemy_peng_headed)

    def bubble_sort_by_distance(self, arr, origin):
        # type: (Union[List[Iceberg], List[PenguinGroup]], Iceberg) -> None
        """Sort an array by it's distance to an iceberg"""
        n = len(arr)

        for i in range(n):

            for j in range(0, n - i - 1):

                if origin.get_turns_till_arrival(arr[j]) > origin.get_turns_till_arrival(
                        arr[j + 1]):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

    def bubble_sort_by_peng(self, arr):
        # type: (Union[List[Iceberg], List[PenguinGroup]]) -> None
        """Sort an array by it's amount of penguins"""
        n = len(arr)

        for i in range(n):

            for j in range(0, n - i - 1):

                if (arr[j].penguin_amount - self.get_peng_directed(arr[j]) >
                        arr[j + 1].penguin_amount - self.get_peng_directed(arr[j + 1])):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
