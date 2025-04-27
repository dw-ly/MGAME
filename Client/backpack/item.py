class Item:
    def __init__(self, item_id, name, desc, type_, stackable=True):
        self.item_id = item_id
        self.name = name
        self.desc = desc
        self.type = type_  # 如consumable, equipment, quest等
        self.stackable = stackable

    @classmethod
    def from_dict(cls, data):
        return cls(
            item_id=data['id'],
            name=data['name'],
            desc=data.get('desc', ''),
            type_=data.get('type', 'consumable'),
            stackable=data.get('stackable', True)
        )

    def to_dict(self):
        return {
            'id': self.item_id,
            'name': self.name,
            'desc': self.desc,
            'type': self.type,
            'stackable': self.stackable
        } 