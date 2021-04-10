"""
主函数
运行场景
退出pygame
"""
import sys


import pygame

from actor.researcher import Researcher
from scene import SceneResult
from scene.lab_scene import LabScene
from scene.field_scene import FieldScene
from scene.flowerPlace_scene import FlowerPlaceScene
from scene.palace_scene import PalaceScene
from scene.tomb_scene import TombScene
from scene.penglai_scene import PenglaiScene
from scene.win_fail_scene import WinFailScene
from scene.new_lab_scene import NewLabScene

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((800,600),0,32)
    pygame.display.set_caption('Find_The_Truth')
    # 在场景外建立研究人员
    researcher = Researcher()

    scene_list = ['LabScene','FieldScene']
    for item in scene_list:
        item_scene = globals()[item](screen,researcher)  # 几个场景的构造函数必须一样
        item_scene.run()
        if item_scene.transitional == "Palace":
            scene_list.append('PalaceScene')
        elif item == 'FieldScene' and item_scene.transitional == "flowerplace":
            scene_list.append('FlowerPlaceScene')
        elif item == 'TombScene' and item_scene.transitional == "penglai":
            scene_list.append('PenglaiScene')
        elif item_scene.transitional == 'newlabscene':
            scene_list.append('NewLabScene')
        elif item == 'PalaceScene' and item_scene.transitional == "penglai":
            scene_list.append('PenglaiScene')
        elif item == 'PalaceScene' and item_scene.transitional == 'flowerplace':
            scene_list.append('FlowerPlaceScene')
        elif item == 'FlowerPlaceScene' and item_scene.transitional == 'penglai':
            scene_list.append('PenglaiScene')
        elif item == 'FlowerPlaceScene' and item_scene.transitional == 'tomb':
            scene_list.append('TombScene')
        if item_scene.scene_result == SceneResult.Fail:
            final_result = SceneResult.Fail
            break
        elif item_scene.scene_result == SceneResult.Win:
            final_result = SceneResult.Win
            break
        elif item_scene.scene_result == SceneResult.Quit:
            final_result = SceneResult.Fail
            break

    win_fail_scene = WinFailScene(final_result)
    win_fail_scene.run(screen)

    pygame.quit()
    sys.exit()


if __name__ =='__main__':
    main()
