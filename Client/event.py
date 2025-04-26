import random

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
        """执行选择并应用效果"""
        if 0 <= choice_index < len(self.choices):
            choice = self.choices[choice_index]
            # 应用选择的效果
            for effect in choice.get('effects', []):
                if effect['type'] == 'attribute':
                    character.update_attribute(effect['attribute'], effect['value'])
                elif effect['type'] == 'item':
                    if effect['action'] == 'add':
                        character.add_item(effect['item'])
                    elif effect['action'] == 'remove':
                        character.remove_item(effect['item'])
                elif effect['type'] == 'relationship':
                    character.update_relationship(effect['character'], effect['value'])
                elif effect['type'] == 'experience':
                    character.gain_experience(effect['amount'])
            
            return choice.get('next_event', None)
        return None

class EventManager:
    def __init__(self):
        self.events = {}  # 存储所有事件
        self.current_event = None
        self.daily_events = []  # 存储日常事件

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
        """处理玩家选择"""
        if self.current_event:
            next_event_id = self.current_event.execute_choice(choice_index, character)
            if next_event_id:
                self.set_current_event(next_event_id)
            else:
                self.current_event = None
            return True
        return False 