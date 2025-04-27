import json
import os
from level_system import LevelSystem

class Character:
    def __init__(self, name):
        self.name = name
        self.attributes = {
            'strength': 5,      # 力量
            'intelligence': 5,  # 智力
            'charm': 5,        # 魅力
            'health': 100,     # 健康
            'money': 1000,     # 金钱
        }
        self.inventory = []    # 物品栏
        self.relationships = {} # 与其他角色的关系
        self.level_system = LevelSystem()  # 等级系统

    def update_attribute(self, attribute, value):
        """更新角色属性"""
        if attribute in self.attributes:
            self.attributes[attribute] += value
            if self.attributes[attribute] < 0:
                self.attributes[attribute] = 0

    def add_item(self, item):
        """添加物品到物品栏"""
        self.inventory.append(item)

    def remove_item(self, item):
        """从物品栏移除物品"""
        if item in self.inventory:
            self.inventory.remove(item)

    def update_relationship(self, character_name, value):
        """更新与其他角色的关系"""
        if character_name in self.relationships:
            self.relationships[character_name] += value
        else:
            self.relationships[character_name] = value

    def gain_experience(self, amount):
        """获得经验值并处理升级"""
        level_up_info = self.level_system.gain_experience(amount)
        if level_up_info['leveled_up']:
            # 升级时更新属性
            for attr, value in level_up_info['attribute_gains'].items():
                self.update_attribute(attr, value)
        return level_up_info

    def get_exp_info(self):
        """获取经验值信息"""
        return self.level_system.get_exp_info()

    def to_dict(self):
        """将角色数据转换为字典用于保存"""
        return {
            'name': self.name,
            'attributes': self.attributes,
            'inventory': self.inventory,
            'relationships': self.relationships,
            'level_system': self.level_system.to_dict()
        }

    def load_from_dict(self, data):
        """从字典加载角色数据"""
        self.name = data.get('name', self.name)
        self.attributes = data.get('attributes', self.attributes)
        self.inventory = data.get('inventory', self.inventory)
        self.relationships = data.get('relationships', self.relationships)
        self.level_system.load_from_dict(data.get('level_system', {})) 