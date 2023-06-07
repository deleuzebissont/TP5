from enum import Enum
import arcade


class AttackAnimation(arcade.Sprite):
    ATTACK_SCALE = 0.50
    ANIMATION_SPEED = 5.0


class AttackType(Enum):
    ROCK = 0,
    PAPER = 1,
    SCISSORS = 2
