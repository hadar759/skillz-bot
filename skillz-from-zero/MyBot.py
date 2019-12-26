from base_bot import BaseBot
from generic_bot import GenericBot

if not __debug__:
    from typing import Optional

bot = None  # type: Optional[BaseBot]


def do_turn(game):
    global bot
    if game.turn == 1:
        first_turn()
        bot.first_turn()
    bot.game = game
    bot.do_turn()


def first_turn():
    global bot
    bot = GenericBot()
