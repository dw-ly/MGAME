import json
import os
from character import Character
from event import Event, EventManager

class GameManager:
    def __init__(self):
        print("[GameManager] __init__ called")
        self.character = None
        self.event_manager = EventManager()
        self.game_state = 'menu'  # menu, playing, paused, game_over
        self.day = 1
        self.max_days = 30
        self.save_file = 'save.json'
        self.load_events()
        print(f"[GameManager] events loaded: {list(self.event_manager.events.keys())}")

    def load_events(self, events_file='events.json'):
        """加载事件数据到事件管理器"""
        print(f"[GameManager] load_events from {events_file}")
        if not os.path.exists(events_file):
            print(f"未找到事件数据文件: {events_file}")
            return
        try:
            with open(events_file, 'r', encoding='utf-8') as f:
                events_data = json.load(f)
            for event_id, event_info in events_data.items():
                event = Event(
                    event_id=event_info['event_id'],
                    description=event_info['description'],
                    choices=event_info['choices']
                )
                self.event_manager.add_event(event)
            print(f"已加载事件数据: {len(self.event_manager.events)} 个事件, keys: {list(self.event_manager.events.keys())}")
        except Exception as e:
            print(f"加载事件数据失败: {e}")

    def start_new_game(self, character_name):
        print(f"[GameManager] start_new_game called with name: {character_name}")
        self.character = Character(character_name)
        print(f"[GameManager] character created: {self.character.name}")
        self.event_manager.set_current_event('start')
        print(f"[GameManager] set_current_event('start'), current_event: {self.event_manager.current_event}")
        self.game_state = 'playing'
        self.day = 1

    def load_game(self, save_file=None):
        """加载游戏"""
        if save_file:
            self.save_file = save_file
            
        if not os.path.exists(self.save_file):
            print("没有找到存档文件，开始新游戏")
            return False
            
        try:
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            
            self.character = Character(save_data['character']['name'])
            self.character.attributes = save_data['character']['attributes']
            self.character.inventory = save_data['character']['inventory']
            self.character.relationships = save_data['character']['relationships']
            self.character.experience = save_data['character']['experience']
            self.character.level = save_data['character']['level']
            
            self.day = save_data['day']
            self.event_manager.set_current_event(save_data['current_event'])
            self.game_state = 'playing'
            print("游戏加载成功！")
            return True
        except Exception as e:
            print(f"加载游戏失败: {e}")
            return False

    def save_game(self, save_file=None):
        """保存游戏"""
        if save_file:
            self.save_file = save_file
            
        if not self.character:
            print("没有可保存的游戏数据")
            return False
            
        try:
            save_data = {
                'character': {
                    'name': self.character.name,
                    'attributes': self.character.attributes,
                    'inventory': self.character.inventory,
                    'relationships': self.character.relationships,
                    'experience': self.character.experience,
                    'level': self.character.level
                },
                'day': self.day,
                'current_event': self.event_manager.current_event.event_id if self.event_manager.current_event else None
            }
            
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=4)
            print("游戏保存成功！")
            return True
        except Exception as e:
            print(f"保存游戏失败: {e}")
            return False

    def process_choice(self, choice_index):
        """处理玩家选择"""
        if self.game_state == 'playing' and self.event_manager.current_event:
            if self.event_manager.process_choice(choice_index, self.character):
                self.day += 1
                if self.day > self.max_days:
                    self.game_state = 'game_over'
                return True
        return False

    def get_current_event(self):
        """获取当前事件"""
        return self.event_manager.current_event

    def get_character_status(self):
        """获取角色状态"""
        if not self.character:
            return None
        return {
            'name': self.character.name,
            'attributes': self.character.attributes,
            'level': self.character.level,
            'experience': self.character.experience,
            'day': self.day
        } 