'''
Author: SunHebin dwlyshb@163.com
Date: 2025-04-27 10:57:36
LastEditors: SunHebin dwlyshb@163.com
LastEditTime: 2025-04-27 10:59:55
FilePath: \MGAME\Client\button.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pygame

class Button:
    def __init__(self, x, y, w, h, text, font, color=(255,255,255), text_color=(0,0,0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

class StartButton(Button):
    def __init__(self, x, y, w, h, font):
        super().__init__(x, y, w, h, "开始", font, color=(255,255,255), text_color=(0,0,0))
    # 可扩展特殊样式或行为 