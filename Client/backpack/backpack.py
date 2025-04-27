import os
from common.config_loader import ConfigLoader
from backpack.item import Item

class Backpack:
    def __init__(self, config_path='config/items.json'):
        self.items = {}  # {item_id: {'item': Item, 'count': int}}
        self.item_config = self.load_item_config(config_path)

    def load_item_config(self, config_path):
        loader = ConfigLoader('items', default_config={})
        data = loader.load()
        # 返回 {id: Item实例}
        return {d['id']: Item.from_dict(d) for d in data.get('items', [])}

    def add_item(self, item_id, count=1):
        if item_id not in self.item_config:
            raise ValueError(f'未知物品: {item_id}')
        if item_id in self.items:
            self.items[item_id]['count'] += count
        else:
            self.items[item_id] = {'item': self.item_config[item_id], 'count': count}

    def remove_item(self, item_id, count=1):
        if item_id in self.items:
            self.items[item_id]['count'] -= count
            if self.items[item_id]['count'] <= 0:
                del self.items[item_id]

    def get_items(self):
        return [{**v['item'].to_dict(), 'count': v['count']} for v in self.items.values()]

    def has_item(self, item_id, count=1):
        return item_id in self.items and self.items[item_id]['count'] >= count

    def clear(self):
        self.items.clear() 