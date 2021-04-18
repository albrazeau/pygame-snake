import pygame
import random


def new_food(screen_width, screen_height, food_size, snake):
    food = pygame.Rect(
        random.randint(0, screen_width - food_size),
        random.randint(0, screen_height - food_size),
        food_size,
        food_size,
    )

    while snake.collide_other(food):
        food = pygame.Rect(
            random.randint(0, screen_width - food_size),
            random.randint(0, screen_height - food_size),
            food_size,
            food_size,
        )

    return food


class Snake:
    def __init__(self, screen_width, screen_height, size, color=(255, 255, 255)):
        self.size = size
        self.color = color

        self.body = [
            pygame.Rect(screen_width / 2 - self.size / 2, screen_height / 2 - self.size / 2, self.size, self.size)
        ]

        self.direction = "up"

    def draw(self, screen):
        for rect in self.body:
            pygame.draw.rect(screen, self.color, rect)

    def collide_other(self, other):
        if any(rect.colliderect(other) for rect in self.body):
            return True
        return False

    def collide_self(self):
        if len(self.body) > 15:
            if any(rect.colliderect(self.body[0]) for rect in self.body[15:]):
                return True
        return False

    def position_snapshot(self):
        return [rect.center for rect in self.body]

    def move(self, amount):

        pre_movement_positions = self.position_snapshot()

        if self.direction == "up":
            self.body[0].centery -= amount

        elif self.direction == "down":
            self.body[0].centery += amount

        elif self.direction == "left":
            self.body[0].centerx -= amount

        elif self.direction == "right":
            self.body[0].centerx += amount

        else:
            raise RuntimeError(f"Illegal direction: `{self.direction}`")

        if len(self.body) > 1:
            for i in range(1, len(self.body)):
                self.body[i].center = pre_movement_positions[i - 1]

    def add_tail(self):
        """
        add a new snake rectangle to the body.
        doesnt metter where it does (0, 0) because it will be repositioned with snake.move()
        """
        self.body.append(pygame.Rect(0, 0, self.size, self.size))
