'''
Author: SunHebin dwlyshb@163.com
Date: 2025-04-27 09:49:45
LastEditors: SunHebin dwlyshb@163.com
LastEditTime: 2025-04-27 10:28:46
FilePath: \MGAME\Client\level_system.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
import os
from common.config_loader import ConfigLoader

class LevelSystem:
    def __init__(self):
        self.level = 1
        self.experience = 0
        self.config_loader = ConfigLoader('level_config', {
            "level_requirements": {"1": 50},
            "level_up_attributes": {
                "1": {
                    "strength": 1,
                    "intelligence": 1,
                    "charm": 1,
                    "health": 5,
                    "money": 200
                }
            }
        })
        self.level_config = self.config_loader.load()

    def gain_experience(self, amount):
        """获得经验值"""
        self.experience += amount
        return self.check_level_up()

    def check_level_up(self):
        """检查是否升级，返回升级信息"""
        level_up_info = {
            'leveled_up': False,
            'old_level': self.level,
            'new_level': self.level,
            'attribute_gains': {}
        }

        while True:
            next_level = str(self.level + 1)
            if next_level not in self.level_config["level_requirements"]:
                break
                
            required_exp = self.level_config["level_requirements"][next_level]
            if self.experience >= required_exp:
                self.level += 1
                self.experience -= required_exp
                level_up_info['leveled_up'] = True
                level_up_info['new_level'] = self.level
                # 记录属性提升
                level_up_info['attribute_gains'] = self.level_config["level_up_attributes"][next_level].copy()
            else:
                break

        return level_up_info

    def get_required_exp(self):
        """获取升级所需经验值"""
        next_level = str(self.level + 1)
        if next_level in self.level_config["level_requirements"]:
            return self.level_config["level_requirements"][next_level]
        return None

    def get_exp_info(self):
        """获取经验值信息"""
        return {
            'current_exp': self.experience,
            'required_exp': self.get_required_exp(),
            'level': self.level
        }

    def get_level_up_attributes(self):
        """获取升级时的属性提升值"""
        next_level = str(self.level + 1)
        if next_level in self.level_config["level_up_attributes"]:
            return self.level_config["level_up_attributes"][next_level]
        return None

    def to_dict(self):
        """将等级系统数据转换为字典，用于保存"""
        return {
            'level': self.level,
            'experience': self.experience
        }

    def load_from_dict(self, data):
        """从字典加载等级系统数据"""
        self.level = data.get('level', 1)
        self.experience = data.get('experience', 0) 