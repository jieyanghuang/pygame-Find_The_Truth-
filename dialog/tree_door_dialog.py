import pygame
import os
from dialog import blit_text


class TreeDoorDialog:
    def __init__(self, numbertext):
        dialog_path = os.path.join("resource1", 'dialog_one.png')
        temp_dialog = pygame.image.load(dialog_path)
        dialog_w = temp_dialog.get_width() // 2
        dialog_h = temp_dialog.get_height() // 2
        self.dialog = pygame.transform.scale(temp_dialog, (dialog_w, dialog_h))
        font_path = os.path.join("resource1",'font','迷你简粗宋.TTF')
        font = pygame.font.Font(font_path,18)
        if numbertext == 1:
            text = "你看到了地上有个果实，是否食用 A(食用)/B(不食用)"
        elif numbertext == 2:
            text = "果实有毒，你中毒而亡"

        blit_text(self.dialog,text,(20,25),font)  # 设置文章段落格式

        # 设置框架的宽高
        self.surface = pygame.Surface((dialog_w,dialog_h)) #默认生成黑图片
        # 设置关键色为透明，否则为全黑
        self.surface.set_colorkey((0,0,0))

    def draw(self, surface):
        surface.blit(self.dialog, (0, 0))