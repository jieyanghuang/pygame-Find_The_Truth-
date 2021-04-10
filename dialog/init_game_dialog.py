import pygame
import os

from dialog import blit_text


class InitGameDialog:
    def __init__(self, numbertext):
        # 加载人物头像，并修改宽高
        dialog_path = os.path.join("resource1", 'dialog_two.png')
        temp_dialog = pygame.image.load(dialog_path)
        dialog_w = temp_dialog.get_width() // 2
        dialog_h = temp_dialog.get_height() // 2
        dialog = pygame.transform.scale(temp_dialog, (dialog_w, dialog_h))
        font_path = os.path.join("resource1", 'font', '迷你简粗宋.TTF')
        font = pygame.font.Font(font_path, 20)
        if numbertext == 1:
            text = "           欢迎来到find_the_truth游戏!           "\
                   "                                       " \
                   " 现在是23世纪，你是国家历史研究院的一名研究人员" \
                   " 你将乘坐时光穿越机前往唐朝寻找历史信息来帮助教" \
                   " 授研究历史人物杨贵妃的死因,穿越器有时间限制，在" \
                   " 唐朝，你最多只能去往四个地方"\
                   " 游戏成功条件为你成功穿越回来并带回有用的资料 Y/N"
        else:
            text = "无"

        blit_text(dialog, text, (50, 25), font)  # 设置文章段落格式

        # 设置框架的宽高
        self.surface = pygame.Surface((dialog_w, dialog_h))  # 默认生成黑图片
        # 设置关键色为透明，否则为全黑
        self.surface.set_colorkey((0, 0, 0))
        self.dialog = dialog

    def draw(self, surface):
        surface.blit(self.dialog, (150,80))