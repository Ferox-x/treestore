from typing import Any


class Node:
    def __init__(self, item: dict[str:Any]):
        self.item = item
        self.children = []


class TreeStore:
    def __init__(self, data: list[dict[str:Any]]):
        self.hash = {}
        self.root = None
        for item in data:
            node = Node(item)
            self.hash[item['id']] = node
            if item['parent'] == 'root':
                self.root = node
            else:
                parent = self.hash[item['parent']]
                parent.children.append(node)

    def _get_node(self, item_id: int) -> Node:
        return self.hash[item_id]

    def get_all(self) -> list[dict[str:Any]]:
        return [node.item for node in self.hash.values()]

    def get_item(self, item_id: int) -> dict[str:Any]:
        return self._get_node(item_id).item

    def get_children(self, item_id: int) -> list[dict[str:Any]]:
        parent = self._get_node(item_id)
        return [node.item for node in parent.children]

    def get_all_parents(self, item_id: int) -> list[dict[str:Any]]:
        child = self._get_node(item_id)
        parents = [child.item]
        while True:
            try:
                parent = self._get_node(child.item['parent'])
                parents.append(parent.item)
                child = parent
            except KeyError:
                break
        return parents


items = [
    {'id': 1, 'parent': 'root'},
    {'id': 2, 'parent': 1, 'type': 'test'},
    {'id': 3, 'parent': 1, 'type': 'test'},
    {'id': 4, 'parent': 2, 'type': 'test'},
    {'id': 5, 'parent': 2, 'type': 'test'},
    {'id': 6, 'parent': 2, 'type': 'test'},
    {'id': 7, 'parent': 4, 'type': None},
    {'id': 8, 'parent': 4, 'type': None},
]
ts = TreeStore(items)

result = ts.get_all()
assert result == items

item_7 = {
    'id': 7,
    'parent': 4,
    'type': None,
}
result = ts.get_item(7)
assert result == item_7

children_4 = [
    {'id': 7, 'parent': 4, 'type': None},
    {'id': 8, 'parent': 4, 'type': None},
]
result = ts.get_children(4)
assert result == children_4

children_5 = []
result = ts.get_children(5)
assert result == children_5

parents_7 = [
    {'id': 7, 'parent': 4, 'type': None},
    {'id': 4, 'parent': 2, 'type': 'test'},
    {'id': 2, 'parent': 1, 'type': 'test'},
    {'id': 1, 'parent': 'root'},
]
result = ts.get_all_parents(7)
assert result == parents_7
