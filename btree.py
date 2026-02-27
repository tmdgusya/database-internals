from typing import List, Optional, Set, Tuple

class BTreeNode:
    def __init__(self, is_leaf: bool = True) -> None:
        self.keys: List[int] = []
        self.children: List[BTreeNode] = []
        self.is_leaf = is_leaf
        self.key_count: int = 0

    def insert_key_in_node(self, key: int):
        for i in range(self.key_count):
            if key < self.keys[i]:
                self.keys.insert(i, key)
                self.key_count += 1
                return

        self.keys.append(key)
        self.key_count += 1

class BTree:
    def __init__(self, m: int) -> None:
        self.m = m
        self.root = None
        self.size: int = 0

    def search(self, node: Optional[BTreeNode], key: int) -> Optional[BTreeNode]:
        if node is None:
            return None

        i = 0
        while i < node.key_count and key > node.keys[i]:
            i += 1

        if i < node.key_count and key == node.keys[i]:
            return node

        if node.is_leaf:
            return None

        return self.search(node.children[i], key)

    def create_node(self, key: int) -> BTreeNode:
        node = BTreeNode()
        node.keys.append(key)
        node.key_count += 1

        if self.root is None:
            self.root = node

        return node

    def split_node(self, node: BTreeNode) -> Tuple[int, BTreeNode]:
        mid = node.key_count // 2
        mid_key = node.keys[mid]

        right = BTreeNode(is_leaf=node.is_leaf)
        right.keys = node.keys[mid + 1:]
        right.key_count = len(right.keys)
        right.children = node.children[mid + 1:]

        node.keys = node.keys[:mid]
        node.key_count = len(node.keys)
        node.children = node.children[:mid + 1]

        return mid_key, right

    def put(self, key: int):
        if self.root is None:
            self.root = self.create_node(key)
            self.size += 1
            return

        result = self._insert(self.root, key)
        if result:
            mid_key, right = result
            new_root = BTreeNode(is_leaf=False)
            new_root.keys = [mid_key]
            new_root.key_count = 1
            new_root.children = [self.root, right]
            self.root = new_root
        self.size += 1

    def _insert(self, node: BTreeNode, key: int):
        if node.is_leaf:
            node.insert_key_in_node(key)

            if node.key_count > self.m - 1:
                return self.split_node(node)
            return None

        i = 0
        while i < node.key_count and key > node.keys[i]:
            i += 1

        child = node.children[i]
        result = self._insert(child, key)

        if result:
            mid_key, right = result
            node.keys.insert(i, mid_key)
            node.children.insert(i + 1, right)
            node.key_count += 1

            if node.key_count > self.m - 1:
                return self.split_node(node)
            return None
