import pygame
import os

from dialog import blit_text


class ProfessorDialog:
    def __init__(self, numbertext):
        # 加载人物头像，并修改宽高
        img_path = os.path.join("resource1",'professor_head.png')
        temp_header = pygame.image.load(img_path)
        header_w = temp_header.get_width() //2
        header_h = temp_header.get_height() //2
        header = pygame.transform.scale(temp_header,(header_w,header_h))
        dialog_path = os.path.join("resource1", 'dialog.png')
        temp_dialog = pygame.image.load(dialog_path)
        dialog_w = temp_dialog.get_width() // 2
        dialog_h = temp_dialog.get_height() // 2
        dialog = pygame.transform.scale(temp_dialog, (dialog_w, dialog_h))
        font_path = os.path.join("resource1",'font','迷你简粗宋.TTF')
        font = pygame.font.Font(font_path,18)
        if numbertext == 1:
            text = "研究员，你好，教授拜托你穿 越到唐朝去,找到马嵬驿兵变杨 贵妃死亡的真相"\
               " 你准备好进入时光机了吗？Y/N"
        elif numbertext == 2:
            text = "感谢你带回这封信，这对我们 的研究帮助很大" \
                   "谢谢你 Y/N"
        else:
            text = "很遗憾你没有带回有用的研究 信息 Y/N"

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