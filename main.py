import random

import arcade

from attack_animation import AttackType
from game_state import GameState

# je definis les dimensions de l ecran
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"
DEFAULT_LINE_HEIGHT = 45


class MyGame(arcade.Window):
    # je definis les positions de l image du personnage et de l ordinateur
    PLAYER_IMAGE_X = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)
    PLAYER_IMAGE_Y = SCREEN_HEIGHT / 2.5
    COMPUTER_IMAGE_X = (SCREEN_WIDTH / 2) * 1.5
    COMPUTER_IMAGE_Y = SCREEN_HEIGHT / 2.5
    ATTACK_FRAME_WIDTH = 154 / 2
    ATTACK_FRAME_HEIGHT = 154 / 2

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
# je definis la couleur de l ecran
        arcade.set_background_color(arcade.color.BLACK_OLIVE)
# j associe une valeur nulle a la plupart des variables pour pouvoir les redefinir dans setup
        self.player = None
        self.computer = None
        self.players = None
        self.rock = None
        self.paper = None
        self.scissors = None
        self.rock_bot = None
        self.paper_bot = None
        self.scissors_bot = None
        self.player_score = 0
        self.computer_score = 0
        self.player_attack_type = {}
        self.player_attack_chosen = False
        self.player_won_round = None
        self.draw_round = None
        self.game_state = GameState.NOT_STARTED
        self.computer_attack_type = None

    def setup(self):
        # je redefinis les attributs que j avais cree dans init
        self.player = arcade.Sprite("asssets/faceBeard.png", 0.5, center_x=self.PLAYER_IMAGE_X,
                                    center_y=self.PLAYER_IMAGE_Y)
        self.computer = arcade.Sprite("asssets/compy.png", 2.5, center_x=self.COMPUTER_IMAGE_X,
                                      center_y=self.COMPUTER_IMAGE_Y)
        self.players = arcade.SpriteList()
        self.players.append(self.player)
        self.players.append(self.computer)
        self.player_attack_type = None
        self.computer_attack_type = random.choice([AttackType.ROCK, AttackType.PAPER, AttackType.SCISSORS])
        self.rock = arcade.Sprite("asssets/srock.png", 0.5, center_x=150, center_y=100)
        self.paper = arcade.Sprite("asssets/spaper.png", 0.5, center_x=250, center_y=100)
        self.scissors = arcade.Sprite("asssets/scissors.png", 0.5, center_x=350, center_y=100)
        self.rock_bot = arcade.Sprite("asssets/srock.png", 0.5, center_x=750, center_y=100)
        self.paper_bot = arcade.Sprite("asssets/spaper.png", 0.5, center_x=750, center_y=100)
        self.scissors_bot = arcade.Sprite("asssets/scissors.png", 0.5, center_x=750, center_y=100)
        self.player_attack_chosen = False
        self.draw_round = 0
        self.game_state = GameState.NOT_STARTED

    def validate_victory(self):
        # je definis les conditions de qui gagnera la partie par le choix du joueur et de l ordinateur tout en ajustant
        # le score
        self.draw_computer_attack()
        if self.game_state == GameState.ROUND_ACTIVE:
            if self.computer_attack_type == self.player_attack_type:
                pass
            elif self.player_attack_type == AttackType.ROCK and self.computer_attack_type == AttackType.SCISSORS:
                self.player_score += 1
            elif self.player_attack_type == AttackType.SCISSORS and self.computer_attack_type == AttackType.PAPER:
                self.player_score += 1
            elif self.player_attack_type == AttackType.PAPER and self.computer_attack_type == AttackType.ROCK:
                self.player_score += 1
            else:
                self.computer_score += 1
# si le joueur ou l ordinateur a 3 points, la partie est fini, sinon, une autre round commence
        if self.player_score < 3 and self.computer_score < 3:
            self.game_state = GameState.ROUND_DONE
        else:
            self.game_state = GameState.GAME_OVER
# dependant, du mode de jeu et du choix du joueur, je dessine les attaques possibles
    def draw_possible_attack(self):
        if self.game_state == GameState.ROUND_ACTIVE:
            self.rock.draw()
            self.paper.draw()
            self.scissors.draw()
        elif self.game_state == GameState.ROUND_DONE or self.game_state == GameState.GAME_OVER:
            if self.player_attack_type == AttackType.ROCK:
                self.rock.draw()
            elif self.player_attack_type == AttackType.PAPER:
                self.paper.draw()
            elif self.player_attack_type == AttackType.SCISSORS:
                self.scissors.draw()

    # dependant, du mode de jeu et du choix de l ordinateur, je dessine l'attaque choisi
    def draw_computer_attack(self):
        if self.game_state == GameState.ROUND_ACTIVE:
            self.rock_bot.draw()
            self.paper_bot.draw()
            self.scissors_bot.draw()
        elif self.game_state == GameState.ROUND_DONE or self.game_state == GameState.GAME_OVER:
            if self.computer_attack_type == AttackType.ROCK:
                self.rock_bot.draw()
            elif self.computer_attack_type == AttackType.PAPER:
                self.paper_bot.draw()
            elif self.computer_attack_type == AttackType.SCISSORS:
                self.scissors_bot.draw()
# j ecris les instructions dependant du stade de la partie pour donner des instructions aux joueurs
    def draw_instructions(self):
        arcade.draw_text(f"Score du joueur : {self.player_score}, Score de l'ordi : {self.computer_score}", 0, 350,
                         arcade.color.BABY_BLUE_EYES, 15, width=SCREEN_WIDTH, align="center")
        if self.game_state == GameState.NOT_STARTED:
            arcade.draw_text('Appuyez sur espace pour commencer.', 0, 400, arcade.color.BLIZZARD_BLUE, 20,
                             width=SCREEN_WIDTH, align="center")
        elif self.game_state == GameState.ROUND_ACTIVE:
            arcade.draw_text('Veuillez appuyer sur votre choix.', 0, 400, arcade.color.BLIZZARD_BLUE, 20,
                             width=SCREEN_WIDTH, align="center")
        elif self.game_state == GameState.ROUND_DONE:
            arcade.draw_text("Veuillez appuyer sur ESPACE pour recommencer une round !", 0, 400,
                             arcade.color.BLIZZARD_BLUE, 20,
                             width=SCREEN_WIDTH, align="center")
        elif self.game_state == GameState.GAME_OVER:
            arcade.draw_text("La partie est fini,appuyez sur ESPACE pour faire une nouvelle partie !", 0, 400,
                             arcade.color.BLIZZARD_BLUE, 20,
                             width=SCREEN_WIDTH, align="center")
            if self.player_score == 3:
                arcade.draw_text("Vous avez gagné !", 0, 450,
                                 arcade.color.BLIZZARD_BLUE, 20,
                                 width=SCREEN_WIDTH, align="center")

            elif self.computer_score == 3:
                arcade.draw_text("Vous avez perdu !", 0, 450,
                                 arcade.color.BLIZZARD_BLUE, 20,
                                 width=SCREEN_WIDTH, align="center")


    def on_draw(self):
# je donne son titre a l ecran
        arcade.start_render()
        arcade.draw_text(SCREEN_TITLE,
                         0,
                         SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,
                         arcade.color.BLACK_BEAN,
                         60,
                         width=SCREEN_WIDTH,
                         align="center")

        self.draw_instructions()
# je dessine les rectangles ou les images se trouveront
        self.players.draw()
        arcade.draw_rectangle_outline(150, 100, self.ATTACK_FRAME_WIDTH,
                                      self.ATTACK_FRAME_HEIGHT, arcade.color.RED, 5)
        arcade.draw_rectangle_outline(250, 100, self.ATTACK_FRAME_WIDTH,
                                      self.ATTACK_FRAME_HEIGHT, arcade.color.RED, 5)
        arcade.draw_rectangle_outline(350, 100, self.ATTACK_FRAME_WIDTH,
                                      self.ATTACK_FRAME_HEIGHT, arcade.color.RED, 5)
        arcade.draw_rectangle_outline(750, 100, self.ATTACK_FRAME_WIDTH,
                                      self.ATTACK_FRAME_HEIGHT, arcade.color.RED, 5)
# j execute les differentes fonctions dependamment de quelle mode de jeu est actif
        if self.game_state == GameState.ROUND_ACTIVE:
            self.draw_possible_attack()
        elif self.game_state == GameState.ROUND_DONE or self.game_state == GameState.GAME_OVER:
            self.draw_possible_attack()
            self.draw_computer_attack()

    # je choisi l attaque de l ordinateur
    def choose_computer_attack(self):
        self.computer_attack_type = random.choice(list(AttackType))

    def on_key_press(self, key, key_modifiers):
        # si on appuie sur differentes touches a differents moments, le stade de jeu change
        if self.game_state == GameState.NOT_STARTED and key == arcade.key.SPACE:
            self.game_state = GameState.ROUND_ACTIVE
        elif self.game_state == GameState.ROUND_DONE and key == arcade.key.SPACE:
            self.game_state = GameState.ROUND_ACTIVE
            self.reset_round()
        elif self.game_state == GameState.GAME_OVER and key == arcade.key.SPACE:
            self.reset_game()

    def reset_round(self):
        # nous effacons les donnes importantes lorsque le stade de jeu est definis a ROUND_DONE
        self.computer_attack_type = False
        self.player_attack_chosen = False

    def reset_game(self):
        # nous effacons les donnees importantes lorsque le stade de jeu est definis a GAME_OVER
        self.game_state = GameState.ROUND_ACTIVE
        self.player_score = 0
        self.computer_score = 0
        self.reset_round()

    def on_mouse_press(self, x, y, button, key_modifiers):
        # si l on appuie sur differents icones, l attaque du joueur change
        if self.game_state == GameState.ROUND_ACTIVE:
            if self.rock.collides_with_point((x, y)):
                self.player_attack_type = AttackType.ROCK
                self.player_attack_chosen = True
            elif self.paper.collides_with_point((x, y)):
                self.player_attack_type = AttackType.PAPER
                self.player_attack_chosen = True
            elif self.scissors.collides_with_point((x, y)):
                self.player_attack_type = AttackType.SCISSORS
                self.player_attack_chosen = True
            self.choose_computer_attack()
            self.validate_victory()


def main():
    # nous definissons la fonction que nous allons executer pour lancer notre jeu
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    # nous executons la fonction
    main()

