import pygame
import time

class BasePopup:
    def __init__(self, ui, text, color=(0, 255, 0), width=320, top=False):
        self.ui = ui  # 传入BaseUI实例
        self.text = text
        self.color = color
        self.width = width
        self.top = top
        self.lines = self.wrap_text(text, width-40)
        self.line_height = 28
        self.height = 40 + len(self.lines) * self.line_height + 60
        self.rect = self.get_rect()

    def wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        font = self.ui.font
        for word in words:
            test_line = current_line + (' ' if current_line else '') + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        # 兼容中文
        final_lines = []
        for line in lines:
            if font.size(line)[0] <= max_width:
                final_lines.append(line)
            else:
                temp = ''
                for ch in line:
                    if font.size(temp + ch)[0] <= max_width:
                        temp += ch
                    else:
                        final_lines.append(temp)
                        temp = ch
                if temp:
                    final_lines.append(temp)
        return final_lines

    def get_rect(self):
        screen = self.ui.screen
        if self.top:
            return pygame.Rect(
                screen.get_width()//2 - self.width//2,
                40,
                self.width, self.height
            )
        else:
            return pygame.Rect(
                screen.get_width()//2 - self.width//2,
                screen.get_height()//2 - self.height//2,
                self.width, self.height
            )

    def draw(self):
        raise NotImplementedError

class DialogPopup(BasePopup):
    def draw(self):
        screen = self.ui.screen
        pygame.draw.rect(screen, (30, 30, 30), self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        for i, line in enumerate(self.lines):
            text_surface = self.ui.font.render(line, True, self.color)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.y + 30 + i*self.line_height))
            screen.blit(text_surface, text_rect)
        # 确认按钮
        btn_rect = pygame.Rect(self.rect.centerx-50, self.rect.bottom-50, 100, 35)
        pygame.draw.rect(screen, (255,255,255), btn_rect)
        btn_text = self.ui.font.render("确认", True, (0,0,0))
        btn_text_rect = btn_text.get_rect(center=btn_rect.center)
        screen.blit(btn_text, btn_text_rect)
        pygame.display.flip()
        return btn_rect

class BannerPopup(BasePopup):
    def __init__(self, ui, text, color=(0,255,0), width=320, top=False, duration=1.5):
        super().__init__(ui, text, color, width, top)
        self.start_time = time.time()
        self.duration = duration
    def draw(self):
        screen = self.ui.screen
        pygame.draw.rect(screen, (30, 30, 30), self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        for i, line in enumerate(self.lines):
            text_surface = self.ui.font.render(line, True, self.color)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.y + 30 + i*self.line_height))
            screen.blit(text_surface, text_rect)
        pygame.display.flip()
        # 无需返回按钮
        return None
    def expired(self):
        return (time.time() - self.start_time) > self.duration 