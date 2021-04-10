"""
樱花谷的场景
"""
import os
import pygame
from pygame.constants import QUIT, KEYDOWN, K_y
from pytmx import pytmx
#  from dialog.battle_dialog import BattleDialog, BattleStatus
from actor.maid import Maid
from scene import TiledScene, FadeScene, SceneResult, SceneStatus
from actor.professor import Professor


class PalaceScene:
    """
    宫殿场景
    """

    def __init__(self, surface: pygame.Surface, researcher):
        """
        宫殿场景的初始化
        :param surface: 窗口绘制的surface
        """
        self.surface = surface
        tiled_path = os.path.join('resource1/resource2/ palace.tmx')
        self.tiled = TiledScene(tiled_path)
        # 渐变对象
        self.fade = FadeScene(self.tiled.surface)

        # 创建一个人物
        self.transitional = None
        self.researcher = researcher
        self.pos_x = 0
        self.pos_y = 0
        self.obstacle_group = pygame.sprite.Group()  # 障碍物
        self.maid = None
        self.maid2 = None
        #
        self.init_actor()
        self.temp_surface = pygame.Surface((800, 600))
        # 打斗场景改为空
        # self.battle_dialog = None  # 打斗
        self.scene_result = SceneResult.Ongoing
        pygame.mixer.music.unload()
        sound_path = os.path.join('resource1', 'music', 'palace.wav')
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def init_actor(self):
        """
        9.6初始化角色和人物
        :return:
        """
        for group in self.tiled.tiled.tmx_data.objectgroups:
            if isinstance(group, pytmx.TiledObjectGroup):
                if group.name == "obstacle":
                    for obj in group:
                        obstacle = pygame.sprite.Sprite()
                        obstacle.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.obstacle_group.add(obstacle)
                if group.name == "actor":
                    for obj in group:
                        if obj.name == "researcher":
                            self.researcher.reset_pos(obj.x, obj.y)
                            # 设置窗口位置（子图的初始位置）
                            self.pos_x = obj.x - 400
                            self.pos_y = obj.y - 300
                if group.name == "npc ":
                    for obj in group:
                        if obj.name == "maid":
                            self.maid = Maid(obj.x, obj.y, 1)
                        if obj.name == "maid2":
                            self.maid2 = Maid(obj.x, obj.y, 2)

    def get_current_surface(self) -> pygame.Surface:
        """
        获取当前显示场景的surface
        :return: 当前显示场景的surface
        """
        # 获取子图
        sub_surface = self.fade.get_back_image(self.pos_x, self.pos_y)
        self.temp_surface.blit(sub_surface, (0, 0))
        self.researcher.draw(self.temp_surface, self.pos_x, self.pos_y)
        self.maid.draw(self.temp_surface, self.pos_x, self.pos_y)
        self.maid2.draw(self.temp_surface, self.pos_x, self.pos_y)
        return self.temp_surface

    def run(self):
        """
        场景的运行
        :return:
        """
        scene_exit = False  # 场景最开始不退出
        clock = pygame.time.Clock()
        while not scene_exit:
            Key_down = False
            pressed_key = None
            for event in pygame.event.get():
                if event.type == QUIT:
                    scene_exit = True
                    self.scene_result = SceneResult.Fail
                if event.type == KEYDOWN:
                    Key_down = True
                    pressed_key = event.key
            # 与障碍物碰撞
            if Key_down:
                temp_pos1 = self.researcher.key_move(pressed_key, self.obstacle_group)
                if temp_pos1:
                    self.pos_x += temp_pos1[0]
                    self.pos_y += temp_pos1[1]
                if self.maid.stop and pressed_key == K_y:
                    self.transitional = 'flowerplace'
                    self.researcher.scene_palace = True
                    print(self.researcher.scene_palace)
                    self.fade.set_status(SceneStatus.Out)
                    self.maid.stop = False
                if self.maid2.stop and pressed_key == K_y:
                    self.transitional = 'penglai'
                    self.fade.set_status(SceneStatus.Out)
                    self.maid2.stop = False
            if self.fade.get_out():
                scene_exit = True
            self.maid.collide(self.researcher)
            self.maid2.collide(self.researcher)
            current_screen = self.get_current_surface()
            self.surface.blit(current_screen, (0, 0))
            pygame.display.update()
            clock.tick(10)  # 动画片帧数
        return scene_exit