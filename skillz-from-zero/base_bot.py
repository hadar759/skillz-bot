from abc import ABCMeta, abstractmethod
from penguin_game import *
if not __debug__:
    from typing import Optional


class BaseBot(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.game = None  # type: Optional[Game]

    @abstractmethod
    def do_turn(self):
        pass

    def first_turn(self):
        pass
