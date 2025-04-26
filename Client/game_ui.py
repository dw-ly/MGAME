import pygame
import sys
import os
from game_manager import GameManager
from common.logger import info, no_print

class BaseUI:
    def __init__(self, width=900, height=700, title="文字选择养成游戏"):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        font_path = None
        for candidate in ["simhei.ttf", "msyh.ttc", "msyh.ttf"]:
            if os.path.exists(candidate):
                font_path = candidate
                break
        if font_path:
            try:
                self.font = pygame.font.Font(font_path, 24)
            except Exception:
                self.font = pygame.font.Font(None, 24)
        else:
            self.font = pygame.font.Font(None, 24)

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_button(self, text, x, y, width, height, color):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
        self.screen.blit(text_surface, text_rect)
        return pygame.Rect(x, y, width, height)

    def draw_popup(self, text, color=(0, 255, 0)):
        lines = text.split('\n')
        line_height = 28
        popup_width = 320
        popup_height = 40 + len(lines) * line_height + 60  # 上下边距+内容+按钮
        popup_rect = pygame.Rect(
            self.screen.get_width()//2 - popup_width//2,
            self.screen.get_height()//2 - popup_height//2,
            popup_width, popup_height
        )
        pygame.draw.rect(self.screen, (30, 30, 30), popup_rect)
        pygame.draw.rect(self.screen, color, popup_rect, 2)
        # 文本
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, color)
            text_rect = text_surface.get_rect(
                center=(popup_rect.centerx, popup_rect.y + 30 + i*line_height)
            )
            self.screen.blit(text_surface, text_rect)
        # 确认按钮
        btn_rect = pygame.Rect(
            popup_rect.centerx-50,
            popup_rect.bottom-50,
            100, 35
        )
        pygame.draw.rect(self.screen, (255,255,255), btn_rect)
        btn_text = self.font.render("确认", True, (0,0,0))
        btn_text_rect = btn_text.get_rect(center=btn_rect.center)
        self.screen.blit(btn_text, btn_text_rect)
        pygame.display.flip()
        return btn_rect

class MainMenuUI(BaseUI):
    def __init__(self):
        super().__init__(width=900, height=700)
        self.input_text = ""
        self.input_active = False
        self.input_box_rect = pygame.Rect(250, 570, 400, 40)
        self.show_input_box = False
        self.game_manager = GameManager()
        self.next_ui = None

    def show_menu(self):
        self.screen.fill((0, 0, 0))
        self.draw_text("文字选择养成游戏", 320, 120)
        new_game_rect = self.draw_button("新游戏", 350, 240, 200, 50, (255, 255, 255))
        load_game_rect = self.draw_button("加载游戏", 350, 320, 200, 50, (255, 255, 255))
        quit_rect = self.draw_button("退出", 350, 400, 200, 50, (255, 255, 255))
        if self.show_input_box:
            self.draw_text("请输入角色名称：", 320, 500)
            pygame.draw.rect(self.screen, (255, 255, 255), self.input_box_rect, 2 if self.input_active else 1)
            input_surface = self.font.render(self.input_text, True, (255, 255, 255))
            self.screen.blit(input_surface, (self.input_box_rect.x + 10, self.input_box_rect.y + 5))
            tip = "* 建议切换为英文输入法，否则部分输入法无法输入 *"
            tip_surface = self.font.render(tip, True, (255, 200, 100))
            tip_rect = tip_surface.get_rect(center=(self.screen.get_width() // 2, self.input_box_rect.y + self.input_box_rect.height + 20))
            self.screen.blit(tip_surface, tip_rect)
        pygame.display.flip()
        return new_game_rect, load_game_rect, quit_rect

    def run(self):
        info("[MainMenuUI] run() called")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    info("[MainMenuUI] Quit event")
                    pygame.quit()
                    sys.exit()
                if self.input_active and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.input_text.strip():
                            info(f"[MainMenuUI] Switching to GameMainUI with name: {self.input_text.strip()}")
                            self.next_ui = GameMainUI(self.input_text.strip())
                            return
                        else:
                            self.input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if len(self.input_text) < 12:
                            self.input_text += event.unicode
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    new_game_rect, load_game_rect, quit_rect = self.show_menu()
                    if self.show_input_box and self.input_box_rect.collidepoint(mouse_pos):
                        self.input_active = True
                    elif new_game_rect.collidepoint(mouse_pos):
                        self.show_input_box = True
                        self.input_active = True
                        self.input_text = ""
                    elif load_game_rect.collidepoint(mouse_pos):
                        if self.game_manager.load_game():
                            info(f"[MainMenuUI] Switching to GameMainUI with loaded name: {self.game_manager.character.name}")
                            self.next_ui = GameMainUI(self.game_manager.character.name, self.game_manager)
                            return
                    elif quit_rect.collidepoint(mouse_pos):
                        info("[MainMenuUI] Quit button pressed")
                        pygame.quit()
                        sys.exit()
            self.show_menu()
            self.clock.tick(60)

class GameMainUI(BaseUI):
    def __init__(self, character_name, game_manager=None):
        info(f"[GameMainUI] __init__ with character_name: {character_name}")
        super().__init__(width=900, height=700)
        if game_manager:
            self.game_manager = game_manager
        else:
            self.game_manager = GameManager()
            self.game_manager.start_new_game(character_name)
        self.next_ui = None
        self.save_popup = False
        self.result_popup = False
        self.last_status = None
        self.last_result = None

    def show_game(self):
        if self.game_manager.game_state == 'game_over':
            self.screen.fill((0, 0, 0))
            status = self.game_manager.get_character_status()
            y = 30
            if status:
                self.draw_text(f"游戏结束！", 30, y, (255, 255, 0))
                y += 40
                self.draw_text(f"角色: {status['name']}", 30, y)
                y += 30
                self.draw_text(f"等级: {status['level']}", 30, y)
                y += 30
                self.draw_text(f"经验: {status['experience']}", 30, y)
                y += 30
                self.draw_text(f"天数: {status['day']}/30", 30, y)
                y += 30
                for attr, value in status['attributes'].items():
                    self.draw_text(f"{attr}: {value}", 30, y)
                    y += 30
            quit_rect = self.draw_button("退出", 350, y + 60, 200, 50, (255, 255, 255))
            pygame.display.flip()
            return [quit_rect]
        no_print("[GameMainUI] show_game called")
        self.screen.fill((0, 0, 0))
        status = self.game_manager.get_character_status()
        no_print(f"[GameMainUI] status: {status}")
        y = 30
        if status:
            self.draw_text(f"角色: {status['name']}", 30, y)
            y += 30
            self.draw_text(f"等级: {status['level']}", 30, y)
            y += 30
            self.draw_text(f"经验: {status['experience']}", 30, y)
            y += 30
            self.draw_text(f"天数: {status['day']}/30", 30, y)
            y += 30
            for attr, value in status['attributes'].items():
                self.draw_text(f"{attr}: {value}", 30, y)
                y += 30
        desc_y = y + 30
        current_event = self.game_manager.get_current_event()
        no_print(f"[GameMainUI] current_event: {current_event}")
        choice_rects = []
        if current_event:
            self.draw_text(current_event.description, 30, desc_y)
            btn_y = desc_y + 50
            for i, choice in enumerate(current_event.choices):
                rect = self.draw_button(choice['text'], 80, btn_y, 740, 40, (255, 255, 255))
                choice_rects.append(rect)
                btn_y += 60
            save_rect = self.draw_button("保存游戏", 750, 30, 120, 40, (0, 255, 0))
            choice_rects.append(save_rect)
        if self.save_popup:
            self.draw_popup("保存成功！")
            self.save_popup = False
        if self.result_popup and self.last_result:
            btn_rect = self.draw_popup(self.last_result, color=(255, 255, 0))
            return [btn_rect]
        pygame.display.flip()
        return choice_rects

    def run(self):
        info("[GameMainUI] run() called")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    info("[GameMainUI] Quit event")
                    pygame.quit()
                    sys.exit()
                if self.game_manager.game_state == 'game_over':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        choice_rects = self.show_game()
                        if choice_rects and choice_rects[0].collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()
                    continue
                if self.result_popup and self.last_result:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        btn_rect = self.show_game()[0]
                        if btn_rect.collidepoint(mouse_pos):
                            self.result_popup = False
                            self.last_result = None
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    info(f"[GameMainUI] Mouse click at {mouse_pos}")
                    choice_rects = self.show_game()
                    for i, rect in enumerate(choice_rects):
                        if rect.collidepoint(mouse_pos):
                            if i == len(choice_rects) - 1:
                                info("[GameMainUI] Save game pressed")
                                self.game_manager.save_game()
                                self.save_popup = True
                            else:
                                info(f"[GameMainUI] Choice {i} pressed")
                                # 记录选择前的属性
                                self.last_status = self.game_manager.get_character_status()
                                current_event = self.game_manager.get_current_event()
                                choice = current_event.choices[i]
                                # 处理选择，获取desc
                                ok, desc = self.game_manager.process_choice(i)
                                # 记录选择后的属性
                                new_status = self.game_manager.get_character_status()
                                # 生成属性变化描述
                                changes = []
                                if self.last_status and new_status:
                                    for attr in self.last_status['attributes']:
                                        before = self.last_status['attributes'][attr]
                                        after = new_status['attributes'][attr]
                                        if before != after:
                                            changes.append(f"{attr}: {before} → {after}")
                                    if self.last_status['experience'] != new_status['experience']:
                                        changes.append(f"经验: {self.last_status['experience']} → {new_status['experience']}")
                                    if self.last_status['level'] != new_status['level']:
                                        changes.append(f"等级: {self.last_status['level']} → {new_status['level']}")
                                result_text = f"{desc}\n" + ("\n".join(changes) if changes else "无属性变化")
                                self.last_result = result_text
                                self.result_popup = True
            self.show_game()
            self.clock.tick(60)

def run_app():
    current_ui = MainMenuUI()
    while current_ui:
        info(f"[run_app] Switching to {type(current_ui).__name__}")
        current_ui.run()
        current_ui = getattr(current_ui, 'next_ui', None) 