"""
墓穴的场景
"""
import os
import pygame
from pygame.constants import QUIT, KEYDOWN, K_y, K_LEFT, K_RIGHT, K_UP, KEYUP
from pytmx import pytmx
#  from dialog.battle_dialog import BattleDialog, BattleStatus
from dialog.penglai_door_dialog import PenglaiDoorDialog
from dialog.tomb_letter_dialog import TombLetterDialog
from scene import TiledScene, FadeScene, SceneResult, SceneStatus
from actor.professor import Professor


class TombScene:
    """
    墓穴场景
    """

    def __init__(self, surface: pygame.Surface, researcher):
        """
        墓穴场景的初始化
        :param surface: 窗口绘制的surface
        """
        self.surface = surface
        tiled_path = os.path.join('resource1/resource2/tomb.tmx')
        self.tiled = TiledScene(tiled_path)
        # 渐变对象
        self.fade = FadeScene(self.tiled.surface)

        # 创建一个人物
        self.door = None
        self.penglai_door_dialog = None
        self.transitional = None
        self.letter_dialog_show = True
        self.letter_dialog = None
        self.letter_group = pygame.sprite.Group()
        self.researcher = researcher
        self.pos_x = 0
        self.pos_y = 0
        self.obstacle_group = pygame.sprite.Group()  # 障碍物
        #
        self.init_actor()
        self.temp_surface = pygame.Surface((800, 600))
        # 打斗场景改为空
        # self.battle_dialog = None  # 打斗
        self.scene_result = SceneResult.Ongoing
        pygame.mixer.music.unload()
        sound_path = os.path.join('resource1', 'music', 'tomb.wav')
        pygame.mixer.music.load(sound_path)
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
                if group.name == "npc":
                    for obj in group:
                        if obj.name == "letter":
                            monster = pygame.sprite.Sprite()
                            monster.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            self.letter_group.add(monster)
                if group.name == "door":
                    for obj in group:
                        if obj.name == "door":
                            self.door = pygame.sprite.Sprite()
                            self.door.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

    def get_current_surface(self) -> pygame.Surface:
        """
        获取当前显示场景的surface
        :return: 当前显示场景的surface
        """
        # 获取子图
        sub_surface = self.fade.get_back_image(self.pos_x, self.pos_y)
        self.temp_surface.blit(sub_surface, (0, 0))
        self.researcher.draw(self.temp_surface, self.pos_x, self.pos_y)
        if self.letter_dialog and self.letter_dialog_show:
            self.letter_dialog.draw(self.temp_surface)
        # self.professor.draw(self.temp_surface, self.pos_x, self.pos_y)
        if self.penglai_door_dialog:
            self.penglai_door_dialog.draw(self.temp_surface)

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
            self.create_letter_dialog()
            # 与障碍物碰撞
            self.create_door_dialog()
            if Key_down:
                temp_pos1 = self.researcher.key_move(pressed_key, self.obstacle_group)
                if temp_pos1:
                    self.pos_x += temp_pos1[0]
                    self.pos_y += temp_pos1[1]
                if self.letter_dialog and pressed_key == K_y:
                    self.letter_dialog_show = False
                    self.researcher.pick_letter = 2
                else:
                    self.researcher.pick_letter = 3
                if self.penglai_door_dialog and pressed_key == K_y:
                    self.transitional = "penglai"
                    self.researcher.scene_tomb = True
                    print("self.researcher.scene_tomb ")
                    print(self.researcher.scene_tomb)
                    print("self.scene_palace")
                    print(self.researcher.scene_palace)
                    self.fade.set_status(SceneStatus.Out)
            if self.fade.get_out():
                scene_exit = True
            # self.professor.collide(self.researcher)
            current_screen = self.get_current_surface()
            self.surface.blit(current_screen, (0, 0))
            pygame.display.update()
            clock.tick(10)  # 动画帧数
        return scene_exit

    def create_letter_dialog(self):
        collide_list = pygame.sprite.spritecollide(self.researcher, self.letter_group, False)
        if collide_list:
            self.letter_dialog = TombLetterDialog(1)

    def create_door_dialog(self):
        collide_list = pygame.sprite.collide_rect(self.researcher, self.door)
        if collide_list:
            self.penglai_door_dialog = PenglaiDoorDialog(1)
