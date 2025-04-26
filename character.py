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
        self.experience = 0    # 经验值
        self.level = 1         # 等级

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
        """获得经验值"""
        self.experience += amount
        self.check_level_up()

    def check_level_up(self):
        """检查是否升级"""
        required_exp = self.level * 100
        if self.experience >= required_exp:
            self.level += 1
            self.experience -= required_exp
            return True
        return False 