from btree import BTree


def test_put_single():
    tree = BTree(m=3)
    tree.put(10)
    assert tree.size == 1
    assert tree.root.keys == [10]
    assert tree.root.is_leaf is True


def test_put_without_split():
    tree = BTree(m=3)
    tree.put(10)
    tree.put(20)
    assert tree.root.keys == [10, 20]
    assert tree.size == 2


def test_put_triggers_root_split():
    tree = BTree(m=3)
    for key in [10, 20, 5]:
        tree.put(key)

    # [5, 10, 20] -> 3개 = m개이므로 분할
    # 중간키 10이 루트로, 왼쪽 [5], 오른쪽 [20]
    assert tree.root.keys == [10]
    assert tree.root.is_leaf is False
    assert tree.root.children[0].keys == [5]
    assert tree.root.children[1].keys == [20]
    assert tree.size == 3


def test_put_into_left_child():
    tree = BTree(m=3)
    for key in [10, 20, 5, 3]:
        tree.put(key)

    assert tree.root.keys == [10]
    assert tree.root.children[0].keys == [3, 5]
    assert tree.root.children[1].keys == [20]


def test_put_into_right_child():
    tree = BTree(m=3)
    for key in [10, 20, 5, 15]:
        tree.put(key)

    assert tree.root.keys == [10]
    assert tree.root.children[0].keys == [5]
    assert tree.root.children[1].keys == [15, 20]


def test_put_child_split_propagates():
    tree = BTree(m=3)
    for key in [10, 20, 5, 15, 30]:
        tree.put(key)

    # [15, 20, 30] 오른쪽 자식 분할 -> 20이 루트로 승진
    assert tree.root.keys == [10, 20]
    assert tree.root.children[0].keys == [5]
    assert tree.root.children[1].keys == [15]
    assert tree.root.children[2].keys == [30]


def test_put_double_root_split():
    tree = BTree(m=3)
    for key in [10, 20, 5, 15, 30, 25, 35]:
        tree.put(key)

    # 루트가 두 번 분할되어 높이 3
    assert tree.root.is_leaf is False
    assert tree.size == 7

    # 모든 키를 search로 확인
    for key in [10, 20, 5, 15, 30, 25, 35]:
        assert tree.search(tree.root, key) is not None


def test_search_found():
    tree = BTree(m=4)
    for key in [10, 20, 30, 5, 15, 25]:
        tree.put(key)

    for key in [10, 20, 30, 5, 15, 25]:
        result = tree.search(tree.root, key)
        assert result is not None
        assert key in result.keys


def test_search_not_found():
    tree = BTree(m=4)
    for key in [10, 20, 30]:
        tree.put(key)

    assert tree.search(tree.root, 99) is None
    assert tree.search(tree.root, 1) is None


def test_search_empty_tree():
    tree = BTree(m=3)
    assert tree.search(tree.root, 10) is None


def test_put_order_4():
    tree = BTree(m=4)
    for key in range(1, 11):
        tree.put(key)

    assert tree.size == 10
    for key in range(1, 11):
        assert tree.search(tree.root, key) is not None


def test_put_descending_order():
    tree = BTree(m=3)
    for key in [50, 40, 30, 20, 10]:
        tree.put(key)

    assert tree.size == 5
    for key in [10, 20, 30, 40, 50]:
        assert tree.search(tree.root, key) is not None


def test_all_leaves_same_depth():
    tree = BTree(m=3)
    for key in range(1, 20):
        tree.put(key)

    def get_leaf_depths(node, depth=0):
        if node.is_leaf:
            return [depth]
        depths = []
        for child in node.children:
            depths.extend(get_leaf_depths(child, depth + 1))
        return depths

    depths = get_leaf_depths(tree.root)
    assert len(set(depths)) == 1, f"리프 깊이가 다름: {depths}"
