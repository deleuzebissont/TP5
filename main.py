import random

import arcade

from attack_animation import AttackType, AttackAnimation
from game_state import GameState

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"
DEFAULT_LINE_HEIGHT = 45


class MyGame(arcade.Window):
    PLAYER_IMAGE_X = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)
    PLAYER_IMAGE_Y = SCREEN_HEIGHT / 2.5
    COMPUTER_IMAGE_X = (SCREEN_WIDTH / 2) * 1.5
    COMPUTER_IMAGE_Y = SCREEN_HEIGHT / 2.5
    ATTACK_FRAME_WIDTH = 154 / 2
    ATTACK_FRAME_HEIGHT = 154 / 2

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

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
        """
        Configurer les variables de votre jeu ici. Il faut appeler la méthode une nouvelle
        fois si vous recommencer une nouvelle partie.
        """
        # C'est ici que vous allez créer vos listes de sprites et vos sprites.
        # Prenez note que vous devriez attribuer une valeur à tous les attributs créés dans __init__

    def validate_victory(self):
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

        if self.player_score < 3 and self.computer_score < 3:
            self.game_state = GameState.ROUND_DONE
        else:
            self.game_state = GameState.GAME_OVER

    def draw_possible_attack(self):
        if self.player_attack_type == AttackType.ROCK or self.player_attack_chosen == False:
            self.rock.draw()
        if self.player_attack_type == AttackType.PAPER or self.player_attack_chosen == False:
            self.paper.draw()
        if self.player_attack_type == AttackType.SCISSORS or self.player_attack_chosen == False:
            self.scissors.draw()

    def draw_computer_attack(self):
        if self.computer_attack_type == AttackType.ROCK:
            self.rock_bot.draw()
        elif self.computer_attack_type == AttackType.PAPER:
            self.paper_bot.draw()
        elif self.computer_attack_type == AttackType.SCISSORS:
            self.scissors_bot.draw()

    def draw_scores(self):
        """
      Montrer les scores du joueur et de l'ordinateur
      """
        pass

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
        """
      C'est la méthode que Arcade invoque à chaque "frame" pour afficher les éléments
      de votre jeu à l'écran.
      """

        # Cette commande permet d'effacer l'écran avant de dessiner. Elle va dessiner l'arrière
        # plan selon la couleur spécifié avec la méthode "set_background_color".
        arcade.start_render()

        # Display title
        arcade.draw_text(SCREEN_TITLE,
                         0,
                         SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,
                         arcade.color.BLACK_BEAN,
                         60,
                         width=SCREEN_WIDTH,
                         align="center")

        self.draw_instructions()

        self.players.draw()
        arcade.draw_rectangle_outline(150, 100, self.ATTACK_FRAME_WIDTH,
                                      self.ATTACK_FRAME_HEIGHT, arcade.color.RED, 5)
        arcade.draw_rectangle_outline(250, 100, self.ATTACK_FRAME_WIDTH,
                                      self.ATTACK_FRAME_HEIGHT, arcade.color.RED, 5)
        arcade.draw_rectangle_outline(350, 100, self.ATTACK_FRAME_WIDTH,
                                      self.ATTACK_FRAME_HEIGHT, arcade.color.RED, 5)
        arcade.draw_rectangle_outline(750, 100, self.ATTACK_FRAME_WIDTH,
                                      self.ATTACK_FRAME_HEIGHT, arcade.color.RED, 5)
        if self.game_state == GameState.ROUND_ACTIVE:
            self.draw_possible_attack()

    def on_update(self, delta_time):
        pass

    def choose_computer_attack(self):
        self.computer_attack_type = random.choice([AttackType.ROCK, AttackType.PAPER, AttackType.SCISSORS])

        # vérifier si le jeu est actif (ROUND_ACTIVE) et continuer l'animation des attaques
        # si le joueur a choisi une attaque, générer une attaque de l'ordinateur et valider la victoire
        # changer l'état de jeu si nécessaire (GAME_OVER)
        pass

    def on_key_press(self, key, key_modifiers):
        if self.game_state == GameState.NOT_STARTED and key == arcade.key.SPACE:
            self.game_state = GameState.ROUND_ACTIVE
        elif self.game_state == GameState.ROUND_DONE and key == arcade.key.SPACE:
            self.game_state = GameState.ROUND_ACTIVE
            self.reset_round()
        elif self.game_state == GameState.GAME_OVER and key == arcade.key.SPACE:
            self.reset_game()

    def reset_round(self):
        """
      Réinitialiser les variables qui ont été modifiées
      """
        self.computer_attack_type = False
        self.player_attack_chosen = False
        self.player_attack_type = {AttackType.ROCK: False, AttackType.PAPER: False, AttackType.SCISSORS: False}

    def reset_game(self):
        self.game_state = GameState.NOT_STARTED
        self.player_score = 0
        self.computer_score = 0
        self.computer_attack_type = False
        self.player_attack_chosen = False
        self.player_attack_type = {AttackType.ROCK: False, AttackType.PAPER: False, AttackType.SCISSORS: False}

    def on_mouse_press(self, x, y, button, key_modifiers):
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
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
