import json
import os
from character import Character
from event import Event, EventManager
from common.logger import info, error
import random
from common.save_manager import SaveManager

class GameManager:
    def __init__(self):
        info("[GameManager] __init__ called")
        self.character = None
        self.event_manager = EventManager()
        self.game_state = 'menu'  # menu, playing, paused, game_over
        self.day = 1
        self.max_days = 30
        self.save_manager = SaveManager('save', default_save={})
        info(f"[GameManager] events loaded: {list(self.event_manager.events.keys())}")

    def load_events(self, events_file=None):
        """加载事件数据到事件管理器"""
        if events_file is None:
            events_file = os.path.join(os.path.dirname(__file__), 'config', 'events.json')
        info(f"[GameManager] load_events from {events_file}")
        if not os.path.exists(events_file):
            error(f"未找到事件数据文件: {events_file}")
            return
        try:
            with open(events_file, 'r', encoding='utf-8') as f:
                events_data = json.load(f)
            # 加载主线事件
            for event_id, event_info in events_data.items():
                if event_id == "events":
                    continue
                event = Event(
                    event_id=event_info['event_id'],
                    description=event_info['description'],
                    choices=event_info['choices']
                )
                self.event_manager.add_event(event)
            # 加载日常事件
            for daily_event in events_data.get("events", []):
                choices = []
                for c in daily_event['choices']:
                    effects = []
                    for k, v in c['effects'].items():
                        if k == 'experience':
                            effects.append({'type': 'experience', 'amount': v})
                        else:
                            effects.append({'type': 'attribute', 'attribute': k, 'value': v})
                    choices.append({'text': c['text'], 'effects': effects})
                event = Event(
                    event_id=str(daily_event['id']),
                    description=daily_event['description'],
                    choices=choices
                )
                self.event_manager.add_daily_event(event)
            info(f"已加载事件数据: {len(self.event_manager.events)} 个主线事件, {len(self.event_manager.daily_events)} 个日常事件")
        except Exception as e:
            error(f"加载事件数据失败: {e}")

    def start_new_game(self, character_name):
        """开始新游戏"""
        info(f"[GameManager] start_new_game with character_name: {character_name}")
        self.character = Character(character_name)
        self.game_state = 'playing'
        self.day = 1
        self.event_manager.set_current_event('start')
        return True

    def load_game(self, save_file=None):
        """加载游戏"""
        save_data = self.save_manager.load()
        if not save_data or 'character' not in save_data:
            print("没有找到存档文件，开始新游戏")
            return False
        try:
            char_data = save_data['character']
            self.character = Character(char_data['name'])
            self.character.attributes = char_data['attributes']
            self.character.inventory = char_data['inventory']
            self.character.relationships = char_data['relationships']
            self.character.level_system.level = char_data.get('level', 1)
            self.character.level_system.experience = char_data.get('experience', 0)
            self.day = save_data.get('day', 1)
            self.event_manager.set_current_event(save_data.get('current_event', 'start'))
            self.game_state = 'playing'
            print("游戏加载成功！")
            return True
        except Exception as e:
            print(f"加载游戏失败: {e}")
            return False

    def save_game(self, save_file=None):
        """保存游戏"""
        if not self.character:
            print("没有角色，无法保存")
            return False
        save_data = {
            'character': {
                'name': self.character.name,
                'attributes': self.character.attributes,
                'inventory': self.character.inventory,
                'relationships': self.character.relationships,
                'level': self.character.level_system.level,
                'experience': self.character.level_system.experience
            },
            'day': self.day,
            'current_event': self.event_manager.current_event.event_id if self.event_manager.current_event else None
        }
        return self.save_manager.save(save_data)

    def process_choice(self, choice_index):
        """处理玩家选择，返回desc"""
        if self.game_state == 'playing' and self.event_manager.current_event:
            ok, desc = self.event_manager.process_choice(choice_index, self.character)
            if ok:
                self.day += 1
                # 健康值为0时直接结束游戏
                if self.character.attributes.get('health', 1) <= 0:
                    self.game_state = 'game_over'
                elif self.day > self.max_days:
                    self.game_state = 'game_over'
                # 如果当前事件为空，自动切换到日常事件
                if not self.event_manager.current_event and self.game_state != 'game_over':
                    daily_event = self.event_manager.get_random_daily_event()
                    if daily_event:
                        self.event_manager.current_event = daily_event
                return True, desc
        return False, ''

    def get_current_event(self):
        """获取当前事件"""
        return self.event_manager.current_event

    def get_character_status(self):
        """获取角色状态"""
        if not self.character:
            return None
        exp_info = self.character.get_exp_info()
        return {
            'name': self.character.name,
            'attributes': self.character.attributes,
            'level': exp_info['level'],
            'experience': exp_info['current_exp'],
            'required_exp': exp_info['required_exp'],
            'day': self.day
        } 