import pygame

class InputBox:
    def __init__(self, x, y, w, h, font, max_length=12, text='', active=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (255, 255, 255)
        self.color_active = (255, 255, 0)
        self.color = self.color_inactive
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(self.text, True, (255, 255, 255))
        self.active = active
        self.max_length = max_length

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查是否点击输入框
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 'enter'
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                # 其他按键不处理，交给TEXTINPUT
            elif event.type == pygame.TEXTINPUT:
                if len(self.text) < self.max_length:
                    self.text += event.text
            self.txt_surface = self.font.render(self.text, True, (255, 255, 255))
        return None

    def draw(self, screen):
        # 绘制输入框
        pygame.draw.rect(screen, self.color, self.rect, 3 if self.active else 2)
        # 绘制文本
        txt_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + 5))

    def get_value(self):
        return self.text

    def set_value(self, value):
        self.text = value
        self.txt_surface = self.font.render(self.text, True, (255, 255, 255))

    def set_active(self, active):
        self.active = active
        self.color = self.color_active if self.active else self.color_inactive

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos) 