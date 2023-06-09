from enum import Enum
import arcade

# j associe un nombre a chaque type d attaque
class AttackType(Enum):
    ROCK = 0,
    PAPER = 1,
    SCISSORS = 2
