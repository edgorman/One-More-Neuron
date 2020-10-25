"""Game File
"""
import math
import random
import pygame
from .block import Block
from .ball import Ball

SCREEN_WIDTH = 1205
SCREEN_HEIGHT = 720

GAME_TICK_SPEED = 60

BALL_RADIUS = 10
BALL_START_X = 600
BALL_START_Y = 700

BLOCK_WIDTH = 70
BLOCK_WIDTH_MAX = 16
BLOCK_HEIGHT = 70
BLOCK_HEIGHT_MAX = 9
BLOCK_BETWEEN_GAP = 5
BLOCK_SPAWN_THRESHOLD = 0.75


class Game:
    """ This is the Game class """

    def __init__(self, agent=None, level=0):
        self._clock = None
        self._elapsed = 0
        self._running = True
        self._display_surf = None
        self._score_surf = None

        self.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.blocks = []
        self.balls = []
        self.balls_left = 0
        self.level = level
        self.level_active = False

        self.agent = agent
        self.agent_action = None

    def on_init(self):
        """ this method is called on initialisation """
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("One More Neuron")

        # Set up pygame
        self._clock = pygame.time.Clock()
        self._running = True

        # Set up the display
        self._display_surf = pygame.display.set_mode(self.size)
        self._display_surf.fill(pygame.Color(0, 0, 0))
        self._score_surf = pygame.font.SysFont('Arial', 24)

    def on_event(self, event):
        """ this method is called on an event """
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONUP:
            if not self.level_active:
                # Level is not active
                ball_vec = pygame.math.Vector2(BALL_START_X, BALL_START_Y)
                mouse_vec = pygame.math.Vector2(pygame.mouse.get_pos())
                shot_vec = pygame.math.Vector2(ball_vec - mouse_vec)
                shot_vec.normalize_ip()

                start_time = pygame.time.get_ticks()
                x, y = shot_vec[0], shot_vec[1]
                for ball in self.balls:
                    ball.set_velocity(x, y)
                    ball.set_delay(start_time)

                self.level_active = True

    def on_update(self):
        """ this method is called on each update """

        if self.level_active:
            # Level is active

            # Update balls
            for ball in self.balls:
                if ball.get_delay() <= pygame.time.get_ticks():
                    # ball has pased delay
                    new_x, new_y = ball.get_new_position()
                    max_x, max_y = self.size
                    ball_r = ball.get_radius()
                    invert_x, invert_y = False, False

                    if (new_x - ball_r <= 0 or new_x + ball_r >= max_x) and \
                    (new_y - ball_r <= 0 or new_y + ball_r >= max_y):
                        # ball hit corner of screen
                        invert_x = True
                        invert_y = True
                    elif new_x - ball_r <= 0 or new_x + ball_r >= max_x:
                        # ball hit left or right sides of screen
                        invert_x = True
                    elif new_y - ball_r <= 0 or new_y + ball_r >= max_y:
                        # ball hit top or bottom sides of screen
                        if new_y + ball_r >= max_y:
                            ball.hit_floor()
                        invert_y = True

                    for block in self.blocks:
                        # check ball hitting blocks -> https://stackoverflow.com/a/402010
                        block_center_x, block_center_y = block.get_center_position()
                        block_distance_x, block_distance_y = (
                            abs(new_x - block_center_x),
                            abs(new_y - block_center_y)
                        )

                        if (block_distance_x > (BLOCK_WIDTH/2 + ball.get_radius())) or \
                            (block_distance_y > (BLOCK_HEIGHT/2 + ball.get_radius())):
                            # ball is far beyond block
                            continue
                        elif block_distance_x <= (BLOCK_WIDTH/2):
                            # ball is intersecting in x direction
                            ball.hit_block()
                            block.hit_ball()
                            invert_y = True
                        elif block_distance_y <= (BLOCK_HEIGHT/2):
                            # block is intersection in y direction
                            ball.hit_block()
                            block.hit_ball()
                            invert_x = True
                        else:
                            # block is intersecting ?
                            ball.hit_block()
                            block.hit_ball()
                            if block_distance_x > block_distance_y:
                                invert_x = True
                            else:
                                invert_y = True

                    if ball.get_health() <= 0:
                        ball.reset()
                        self.balls_left -= 1
                    else:
                        if invert_x:
                            ball.invert_x_velocity()
                        if invert_y:
                            ball.invert_y_velocity()
                        new_x, new_y = ball.get_new_position()
                        ball.set_position((new_x, new_y))

            # Update blocks
            for block in list(self.blocks):
                if block.get_health() <= 0:
                    self.blocks.remove(block)
        else:
            # Level is not active

            if self.agent is not None:
                # Get input from agent
                self.agent_action = self.agent.on_round_start(self.blocks)
                shot_rad = math.radians(self.agent_action)
                shot_vec = pygame.math.Vector2(math.cos(shot_rad), math.sin(shot_rad))
                shot_vec.normalize_ip()

                start_time = pygame.time.get_ticks()
                x, y = shot_vec[0], shot_vec[1]
                for ball in self.balls:
                    ball.set_velocity(x, y)
                    ball.set_delay(start_time)

                self.level_active = True

        if self.balls_left <= 0:
            # Level has finished
            self.level += 1
            self.level_active = False

            # Generate new ball
            self.balls.append(
                Ball(
                    BALL_START_X,
                    BALL_START_Y,
                    BALL_RADIUS,
                    self.level,
                    (255, 255, 255)
                )
            )
            self.balls_left = len(self.balls)

            # Generate new blocks
            for index in range(BLOCK_WIDTH_MAX):
                if random.random() <= BLOCK_SPAWN_THRESHOLD:
                    self.blocks.append(
                        Block(
                            index,
                            -1,
                            BLOCK_WIDTH,
                            BLOCK_HEIGHT,
                            BLOCK_BETWEEN_GAP,
                            self.level,
                            (255, 255, 255)
                        )
                    )

            # Move blocks down
            for block in self.blocks:
                block.move_down()

            if self.agent is not None:
                # Update agent
                self.agent.on_round_end(
                    self.blocks,
                    self.balls,
                    self.agent_action
                )

        # Check if a block has reached the end
        for block in self.blocks:
            _, y = block.get_position()
            if y >= BLOCK_HEIGHT_MAX:
                # End game
                if self.agent is not None:
                    # If agent training not complete
                    if self.agent.on_game_finish():
                        self.blocks = []
                        self.balls = []
                        self.balls_left = 0
                        self.level = 0
                    else:
                        self._running = False
                else:
                    self._running = False


    def on_render(self):
        """ this method is called on each render """
        self._display_surf.fill(pygame.Color(0, 0, 0))

        # Draw each ball
        for ball in self.balls:
            col_r, col_g, col_b = ball.get_colour()
            x, y = ball.get_position()
            x, y = int(x), int(y)

            pygame.draw.circle(
                self._display_surf,
                pygame.Color(
                    col_r,
                    col_g,
                    col_b
                ),
                (
                    x,
                    y
                ),
                ball.get_radius()
            )

        # Draw each block
        for block in self.blocks:
            block_x, block_y = block.get_coords()
            col_r, col_g, col_b = block.get_colour()

            if block.get_health() <= 0:
                col_a = 0
            else:
                col_a = int((block.get_health() / block.get_original_health()) * 255)

            pygame.draw.rect(
                self._display_surf,
                pygame.Color(
                    col_a,
                    col_a,
                    col_a
                ),
                pygame.Rect(
                    block_x,
                    block_y,
                    BLOCK_WIDTH,
                    BLOCK_HEIGHT
                )
            )

        # Draw text onto screen
        score_surface = self._score_surf.render(
            "One More Neuron;     Level: " + str(self.level),
            False,
            (255, 255, 255)
        )
        self._display_surf.blit(score_surface, (15, SCREEN_HEIGHT - 35))

        # Draw agent text on screen
        if self.agent is not None:
            agent_surface = self._score_surf.render(
                "Agent Name: " + str(self.agent.get_name()) \
                + ";     Game #: " + str(self.agent.get_games_complete()) \
                + ";     Last Reward: " + str(self.agent.get_last_reward()),
                False,
                (255, 255, 255)
            )
            self._display_surf.blit(agent_surface, (SCREEN_WIDTH - 550, SCREEN_HEIGHT - 35))

        # Updates the screen
        pygame.display.flip()

    def on_cleanup(self):
        """ this method is called on exiting """
        pygame.quit()

    def on_start(self):
        """ this method is called at the start of the game """
        self.on_init()

        while self._running:
            # Run game and render loop
            self._clock.tick(GAME_TICK_SPEED)

            if self.agent is None:
                for event in pygame.event.get():
                    self.on_event(event)
            self.on_update()
            self.on_render()

        # Exit game
        self.on_cleanup()
