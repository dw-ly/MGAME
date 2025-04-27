import random
from common.config_loader import ConfigLoader

class Event:
    def __init__(self, event_id, description, choices):
        self.event_id = event_id
        self.description = description
        self.choices = choices  # 选择列表，每个选择包含文本和效果
        self.requirements = {}  # 触发条件
        self.consequences = {}  # 后续事件

    def check_requirements(self, character):
        """检查角色是否满足事件触发条件"""
        for attr, value in self.requirements.items():
            if character.attributes.get(attr, 0) < value:
                return False
        return True

    def execute_choice(self, choice_index, character):
        """执行选择并应用效果，支持多结果描述"""
        if 0 <= choice_index < len(self.choices):
            choice = self.choices[choice_index]
            # 新格式：有results字段
            if 'results' in choice:
                result = random.choice(choice['results'])
                desc = result.get('desc', '')
                effects = result.get('effects', {})
                # 应用effects
                for k, v in effects.items():
                    if k == 'experience':
                        character.gain_experience(v)
                    else:
                        character.update_attribute(k, v)
                return desc, choice.get('next_event', None)
            # 兼容老格式
            desc = ''
            effects = choice.get('effects', {})
            if isinstance(effects, dict):
                # 新格式的effects是字典
                for k, v in effects.items():
                    if k == 'experience':
                        character.gain_experience(v)
                    else:
                        character.update_attribute(k, v)
            elif isinstance(effects, list):
                # 老格式的effects是列表
                for effect in effects:
                    if isinstance(effect, dict):
                        if effect.get('type') == 'attribute':
                            character.update_attribute(effect.get('attribute'), effect.get('value', 0))
                        elif effect.get('type') == 'item':
                            if effect.get('action') == 'add':
                                character.add_item(effect.get('item'))
                            elif effect.get('action') == 'remove':
                                character.remove_item(effect.get('item'))
                        elif effect.get('type') == 'relationship':
                            character.update_relationship(effect.get('character'), effect.get('value', 0))
                        elif effect.get('type') == 'experience':
                            character.gain_experience(effect.get('amount', 0))
            return desc, choice.get('next_event', None)
        return '', None

class EventManager:
    def __init__(self):
        self.events = {}  # 存储所有事件
        self.current_event = None
        self.daily_events = []  # 存储日常事件
        self.config_loader = ConfigLoader('events', {
            "start": {
                "event_id": "start",
                "description": "欢迎来到文字选择养成游戏！今天是你的第一天，你决定...",
                "choices": [
                    {
                        "text": "去图书馆学习",
                        "results": [
                            {"desc": "你在图书馆学到了新知识。", "effects": {"intelligence": 2, "experience": 50}},
                            {"desc": "你在图书馆遇到了一位老师，获得额外经验。", "effects": {"intelligence": 2, "experience": 80}}
                        ],
                        "next_event": "library"
                    }
                ]
            },
            "events": []
        })
        self.load_events()

    def load_events(self):
        """从配置文件加载事件"""
        events_data = self.config_loader.load()
        
        # 加载主线事件
        for event_id, event_info in events_data.items():
            if event_id == "events":
                continue
            event = Event(
                event_id=event_info['event_id'],
                description=event_info['description'],
                choices=event_info['choices']
            )
            self.add_event(event)
            
        # 加载日常事件
        for daily_event in events_data.get("events", []):
            event = Event(
                event_id=f"daily_{daily_event['id']}",
                description=daily_event['description'],
                choices=daily_event['choices']
            )
            self.add_daily_event(event)

    def add_event(self, event):
        """添加新事件"""
        self.events[event.event_id] = event

    def add_daily_event(self, event):
        """添加日常事件"""
        self.daily_events.append(event)

    def get_event(self, event_id):
        """获取指定事件"""
        return self.events.get(event_id)

    def set_current_event(self, event_id):
        """设置当前事件"""
        self.current_event = self.get_event(event_id)

    def get_random_daily_event(self):
        """随机获取一个日常事件"""
        if self.daily_events:
            return random.choice(self.daily_events)
        return None

    def process_choice(self, choice_index, character):
        """处理玩家选择，返回desc"""
        if self.current_event:
            result = self.current_event.execute_choice(choice_index, character)
            if isinstance(result, tuple):
                desc, next_event_id = result
            else:
                desc, next_event_id = '', result
            if next_event_id:
                self.set_current_event(next_event_id)
            else:
                self.current_event = None
            return True, desc
        return False, '' 