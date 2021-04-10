import pygame

from actor import DirAction
from pygame.constants import K_UP, K_DOWN, K_RIGHT, K_LEFT


class Researcher(pygame.sprite.Sprite):
    """
    角色研究人员
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.walk = DirAction("img/researcher",'0423-29dcd4ef-',4, 8, True)
        self.pos_y = 0
        self.pos_x = 0
        self.hp = 100
        self.scene_palace = False
        self.scene_tomb = False
        self.scene = "Lab"
        """
        1：代表初始化
        2：代表拿到信
        3：代表没有拿到信
        """
        self.pick_letter = 1
        self.dir = 0
        self.rect = pygame.Rect(self.pos_x, self.pos_y + 50, 30, 30)

    def reset_pos(self, x, y):
        # 重置角色的位置
        self.pos_x = x
        self.pos_y = y
        self.rect = pygame.Rect(self.pos_x, self.pos_y + 50,30, 30)

    def draw(self, surface, x, y):
        image = self.walk.get_current_image(self.dir)
        surface.blit(image, (self.pos_x - x, self.pos_y - y))

    def key_move(self, key, obstacle_group):
        pos_y = self.pos_y
        pos_x = self.pos_x
        # 计算运动后的坐标
        if key == K_UP:
            self.dir = 2
            pos_y = self.pos_y - 10
            pos_x = self.pos_x - 10
        elif key == K_DOWN:
            self.dir = 0
            pos_x = self.pos_x + 10
            pos_y = self.pos_y + 10
        elif key == K_LEFT:
            self.dir = 1
            pos_x = self.pos_x - 10
            pos_y = self.pos_y + 10
        elif key == K_RIGHT:
            self.dir = 3
            pos_x = self.pos_x + 10
            pos_y = self.pos_y - 10
        else:
            return None

        self.rect = pygame.Rect(pos_x, pos_y + 50, 30, 30)
        collide_list = pygame.sprite.spritecollide(self, obstacle_group, False)

        if len(collide_list) > 0:
            self.rect = pygame.Rect(self.pos_x, self.pos_y + 50,30, 30)
            return None
        else:
            return self.__move__()

    def __move__(self):
        if self.dir == 2:
            x = -10
            y = -10
        elif self.dir == 0:
            x = 10
            y = 10
        elif self.dir == 1:
            x = -10
            y = 10
        elif self.dir == 3:
            x = 10
            y = -10
        self.pos_y += y
        self.pos_x += x
        self.rect = pygame.Rect(self.pos_x, self.pos_y + 50, 30, 30)
        return [x, y]
