import pygame
import os

from dialog import blit_text


class SoldierDialog:
    def __init__(self, numbertext):
        # 加载人物头像，并修改宽高
        img_path = os.path.join("resource1",'head1.tga')
        temp_header = pygame.image.load(img_path)
        header_w = temp_header.get_width() // 2
        header_h = temp_header.get_height() // 2
        header = pygame.transform.scale(temp_header,(header_w,header_h))
        dialog_path = os.path.join("resource1", 'dialog.png')
        temp_dialog = pygame.image.load(dialog_path)
        dialog_w = temp_dialog.get_width() // 2
        dialog_h = temp_dialog.get_height() // 2
        dialog = pygame.transform.scale(temp_dialog, (dialog_w, dialog_h))
        font_path = os.path.join("resource1",'font','迷你简粗宋.TTF')
        font = pygame.font.Font(font_path,18)
        if numbertext == 1:
            text = "是的,当时我在马嵬驿，不过我"\
                   " 认为贵妃脖子上的勒痕不像是 上吊自杀的，像是被人用绳子 弄的，前面的营帐有神奇的力 量能穿越到贵妃的墓冢，说"\
                   " 不定你能找到更多线索"
        else:
            text = "无"

        blit_text(dialog,text,(20,25),font)  # 设置文章段落格式

        # 设置框架的宽高
        if header_h > dialog_h:
            h = header_h
        else:
            h = dialog_h
        w = dialog_w + header_w
        self.surface = pygame.Surface((w,h)) #默认生成黑图片
        # 设置关键色为透明，否则为全黑
        self.surface.set_colorkey((0,0,0))

        self.surface.blit(dialog,(header_w, 0))
        self.surface.blit(header,(0,0))