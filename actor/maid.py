import pygame

from actor import Action
from dialog.maid_dialog import MaidDialog
from dialog.professor_dialog import ProfessorDialog


class Maid(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y,textnumber):
        """
        构造函数
        :param post_x:
        :param pos_y:
        """
        pygame.sprite.Sprite.__init__(self)
        self.action = Action('img/elder/elder2-0000', 6, True)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image_count = 6
        self.width = 40
        self.height = 85
        self.rect = pygame.Rect(pos_x, pos_y, self.width, self.height)
        self.dialog = MaidDialog(textnumber)
        self.stop = False

    def draw(self, surface, x, y):
        """
        绘制函数
        :param surface:背景绘制区域
        :return:
        """
        image = self.action.get_current_image()
        surface.blit(image, (self.pos_x - x, self.pos_y - y))
        if self.stop:
            surface.blit(self.dialog.surface, (self.pos_x - x, self.pos_y - y - 150))

    def collide(self, actor):
        if pygame.sprite.collide_rect(self, actor):
            self.stop = True
        else:
            self.stop = False
