"""
实验室的场景
"""
import os
import pygame
from pygame.constants import QUIT, KEYDOWN, K_y, K_LEFT, K_RIGHT, K_UP, KEYUP, K_n, K_a, K_b
from pytmx import pytmx
#  from dialog.battle_dialog import BattleDialog, BattleStatus
from dialog.house_door_dialog import HouseDoorDialog
from dialog.tree_door_dialog import TreeDoorDialog
from scene import TiledScene, FadeScene, SceneResult, SceneStatus
from actor.professor import Professor


class PenglaiScene:
    """
    实验室场景
    """

    def __init__(self, surface: pygame.Surface, researcher):
        """
        实验室场景的初始化
        :param surface: 窗口绘制的surface
        """
        self.surface = surface
        tiled_path = os.path.join('resource1/resource2/Penglai.tmx')
        self.tiled = TiledScene(tiled_path)
        # 渐变对象
        self.fade = FadeScene(self.tiled.surface)

        # 创建一个人物
        self.tree_dialog_show = True
        self.door_tree = None
        self.door_house = None
        self.door_house_dialog = None
        self.door_tree_dialog1 = None
        self.door_tree_dialog2 = None
        self.transitional = None
        self.collide_list = None
        self.collide_list1 = None
        self.researcher = researcher
        self.pos_x = 0
        self.pos_y = 0
        self.obstacle_group = pygame.sprite.Group()  # 障碍物
        # self.professor = None
        #
        self.init_actor()
        self.temp_surface = pygame.Surface((800, 600))
        # 打斗场景改为空
        # self.battle_dialog = None  # 打斗
        self.scene_result = SceneResult.Ongoing
        pygame.mixer.music.unload()
        sound_path = os.path.join('resource1', 'music', 'penglai.wav')
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)

    def init_actor(self):
        """
        9.6初始化角色和人物
        :return:
        """
        pygame.key.set_repeat(10, 10)  # 长按
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
                if group.name == "door":
                    for obj in group:
                        if obj.name == "tree":
                            self.door_tree = pygame.sprite.Sprite()
                            self.door_tree.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        if obj.name == "house":
                            print("house is a sprite")
                            self.door_house = pygame.sprite.Sprite()
                            self.door_house.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

    def get_current_surface(self) -> pygame.Surface:
        """
        获取当前显示场景的surface
        :return: 当前显示场景的surface
        """
        # 获取子图
        sub_surface = self.fade.get_back_image(self.pos_x, self.pos_y)
        self.temp_surface.blit(sub_surface, (0, 0))
        self.researcher.draw(self.temp_surface, self.pos_x, self.pos_y)
        if self.door_tree_dialog1 and self.tree_dialog_show:
            self.door_tree_dialog1.draw(self.temp_surface)
        if self.door_tree_dialog2:
            self.door_tree_dialog2.draw(self.temp_surface)
        if self.door_house_dialog:
            self.door_house_dialog.draw(self.temp_surface)
        return self.temp_surface

    def run(self):
        """
        场景的运行
        :return:
        """
        scene_exit = False
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
            if self.tree_dialog_show:
                self.create_door_dialog(1)
            self.create_door_house_dialog()
            # 与障碍物碰撞
            if Key_down:
                temp_pos1 = self.researcher.key_move(pressed_key, self.obstacle_group)
                if temp_pos1:
                    self.pos_x += temp_pos1[0]
                    self.pos_y += temp_pos1[1]
                if self.collide_list and pressed_key == K_a:
                    self.create_door_dialog(2)
                    self.scene_result = SceneResult.Fail
                    self.fade.set_status(SceneStatus.Out)
                elif self.collide_list and pressed_key == K_b:
                    self.tree_dialog_show = False
                if self.collide_list1 and pressed_key == K_y:
                    if self.researcher.scene_tomb and self.researcher.scene_palace:
                        self.scene_result = SceneResult.Fail
                        self.fade.set_status(SceneStatus.Out)
                        print("out 执行")
                    else:
                        print("穿越执行")
                        self.transitional = 'newlabscene'
                        self.fade.set_status(SceneStatus.Out)
            if self.fade.get_out():
                scene_exit = True
            current_screen = self.get_current_surface()
            self.surface.blit(current_screen, (0, 0))
            pygame.display.update()
            clock.tick(10)  # 动画片帧数
        return scene_exit

    def create_door_dialog(self, textnumber: int):
        self.collide_list = pygame.sprite.collide_rect(self.researcher, self.door_tree)
        if self.collide_list and textnumber == 1:
            self.door_tree_dialog1 = TreeDoorDialog(textnumber)
        elif textnumber == 2:
            self.door_tree_dialog2 = TreeDoorDialog(textnumber)

    def create_door_house_dialog(self):
        self.collide_list1 = pygame.sprite.collide_rect(self.researcher, self.door_house)
        if self.collide_list1:
            if self.researcher.scene_palace and self.researcher.scene_tomb:
                self.door_house_dialog = HouseDoorDialog(2)
                print("失败框显示")
            else:
                self.door_house_dialog = HouseDoorDialog(1)
