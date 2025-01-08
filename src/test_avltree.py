from typing import Optional
import pytest
from src.interfaces import AVLNodeProtocol, AVLTreeProtocol
from src.AVLTree import AVLTree, AVLNode


def pre_order_keys_recursive(node: Optional[AVLNodeProtocol]) -> list[int]:
    if node is None or not node.is_real_node():
        return []
    assert node.key is not None
    return (
        [node.key]
        + pre_order_keys_recursive(node.left)
        + pre_order_keys_recursive(node.right)
    )


def pre_order_keys(tree: AVLTreeProtocol) -> list[int]:
    return pre_order_keys_recursive(tree.get_root())


@pytest.fixture
def basic_tree_insert() -> AVLTreeProtocol:
    tree: AVLTreeProtocol = AVLTree()
    tree.insert(8, "8")
    tree.insert(4, "4")
    tree.insert(3, "3")
    tree.insert(6, "6")
    tree.insert(15, "15")
    tree.insert(11, "11")
    tree.insert(54, "54")
    assert pre_order_keys(tree) == [8, 4, 3, 6, 15, 11, 54]
    return tree


def test_is_real_node() -> None:
    node: AVLNodeProtocol = AVLNode(None, "Whatever")
    assert not node.is_real_node()
    node.key = 2
    assert node.is_real_node()
    assert AVLNode(5, "value").is_real_node()


def test_search_empty_tree() -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert (None, 0) == tree.search(2)


def test_search_root(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (basic_tree_insert.get_root(), 1) == basic_tree_insert.search(8)


def test_search_middle_node(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    assert (root.left, 2) == basic_tree_insert.search(4)


def test_search_leaf(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    assert (root.right.left, 3) == basic_tree_insert.search(11)


def test_search_not_exsiting_key(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (None, 3) == basic_tree_insert.search(32)
    assert (None, 3) == basic_tree_insert.search(0)


def test_empty_get_root() -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert tree.get_root() is None


def test_empty_after_delete_get_root() -> None:
    tree: AVLTreeProtocol = AVLTree()
    node, _, _ = tree.insert(1, "")
    tree.delete(node)
    assert tree.get_root() is None


def test_full_get_root(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    assert root.key == 8


def test_insert_once_then_search() -> None:
    tree: AVLTreeProtocol = AVLTree()
    tree.insert(1, "val1")
    node, length = tree.search(1)
    assert node is not None and node.key == 1
    assert length == 1


def test_insertsions_increasing_values() -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert pre_order_keys(tree) == []
    assert tree.size() == 0
    assert tree.insert(1, "")[1:] == (0, 0)
    assert pre_order_keys(tree) == [1]
    assert tree.size() == 1
    assert tree.insert(2, "")[1:] == (1, 1)
    assert pre_order_keys(tree) == [1, 2]
    assert tree.insert(3, "")[1:] == (2, 1)
    assert pre_order_keys(tree) == [2, 1, 3]
    assert tree.insert(4, "")[1:] == (2, 2)
    assert pre_order_keys(tree) == [2, 1, 3, 4]
    assert tree.insert(5, "")[1:] == (3, 1)
    assert pre_order_keys(tree) == [2, 1, 4, 3, 5]
    assert tree.insert(6, "")[1:] == (3, 2)
    assert pre_order_keys(tree) == [4, 2, 1, 3, 5, 6]
    assert tree.insert(7, "")[1:] == (3, 1)
    assert pre_order_keys(tree) == [4, 2, 1, 3, 6, 5, 7]
    assert tree.insert(8, "")[1:] == (3, 3)
    assert pre_order_keys(tree) == [4, 2, 1, 3, 6, 5, 7, 8]
    assert tree.size() == 8
    assert (root := tree.get_root()) is not None and root.height == 3


def test_single_left_rotation() -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert pre_order_keys(tree) == []
    tree.insert(1, "")
    assert pre_order_keys(tree) == [1]
    tree.insert(2, "")
    assert pre_order_keys(tree) == [1, 2]
    tree.insert(3, "")
    assert pre_order_keys(tree) == [2, 1, 3]


def test_single_right_rotation() -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert pre_order_keys(tree) == []
    tree.insert(3, "")
    assert pre_order_keys(tree) == [3]
    tree.insert(2, "")
    assert pre_order_keys(tree) == [3, 2]
    tree.insert(1, "")
    assert pre_order_keys(tree) == [2, 1, 3]


def test_double_right_rebalancing() -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert pre_order_keys(tree) == []
    tree.insert(1, "")
    assert pre_order_keys(tree) == [1]
    tree.insert(3, "")
    assert pre_order_keys(tree) == [1, 3]
    tree.insert(2, "")
    assert pre_order_keys(tree) == [2, 1, 3]


def test_double_left_rebalancing() -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert pre_order_keys(tree) == []
    tree.insert(3, "")
    assert pre_order_keys(tree) == [3]
    tree.insert(1, "")
    assert pre_order_keys(tree) == [3, 1]
    tree.insert(2, "")
    assert pre_order_keys(tree) == [2, 1, 3]


def test_finger_search_empty_tree() -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert (None, 0) == tree.finger_search(2)


def test_finger_search_root(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    assert (root, 3) == basic_tree_insert.finger_search(8)


def test_finger_search_middle_node(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    assert (root.left, 4) == basic_tree_insert.finger_search(4)


def test_finger_search_leaf(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    assert (root.right.left, 3) == basic_tree_insert.finger_search(11)


def test_finger_search_not_exsiting_key(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (None, 1) == basic_tree_insert.finger_search(32)
    assert (None, 5) == basic_tree_insert.finger_search(0)


def test_finger_insert_once_then_finger_search() -> None:
    tree: AVLTreeProtocol = AVLTree()
    tree.finger_insert(1, "val1")
    node, length = tree.finger_search(1)
    assert node is not None
    assert node.key == 1
    assert length == 1


def assert_max_node_key(max_node: Optional[AVLNodeProtocol], key: int) -> None:
    assert max_node is not None
    assert max_node.key == key


def test_max_node(basic_tree_insert: AVLTreeProtocol) -> None:
    assert_max_node_key(basic_tree_insert.max_node(), 54)
    basic_tree_insert.insert(70, "")
    assert_max_node_key(basic_tree_insert.max_node(), 70)
    basic_tree_insert.insert(30, "")
    assert_max_node_key(basic_tree_insert.max_node(), 70)


def test_finger_insertsions_increasing_values() -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert pre_order_keys(tree) == []
    assert tree.size() == 0
    assert tree.finger_insert(1, "")[1:] == (0, 0)
    assert pre_order_keys(tree) == [1]
    assert tree.size() == 1
    assert tree.finger_insert(2, "")[1:] == (1, 1)
    assert pre_order_keys(tree) == [1, 2]
    assert tree.finger_insert(3, "")[1:] == (1, 1)
    assert pre_order_keys(tree) == [2, 1, 3]
    assert tree.finger_insert(4, "")[1:] == (1, 2)
    assert pre_order_keys(tree) == [2, 1, 3, 4]
    assert tree.finger_insert(5, "")[1:] == (1, 1)
    assert pre_order_keys(tree) == [2, 1, 4, 3, 5]
    assert tree.finger_insert(6, "")[1:] == (1, 2)
    assert pre_order_keys(tree) == [4, 2, 1, 3, 5, 6]
    assert tree.finger_insert(7, "")[1:] == (1, 1)
    assert pre_order_keys(tree) == [4, 2, 1, 3, 6, 5, 7]
    assert tree.finger_insert(8, "")[1:] == (1, 3)
    assert pre_order_keys(tree) == [4, 2, 1, 3, 6, 5, 7, 8]
    assert tree.size() == 8


def test_finger_search_brother(basic_tree_insert: AVLTreeProtocol) -> None:
    assert basic_tree_insert.finger_search(11)[1] == 3


def test_finger_search_through_root(basic_tree_insert: AVLTreeProtocol) -> None:
    assert basic_tree_insert.finger_search(3)[1] == 5


def test_single_left_rotation_finger() -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert pre_order_keys(tree) == []
    tree.finger_insert(1, "")
    assert pre_order_keys(tree) == [1]
    tree.finger_insert(2, "")
    assert pre_order_keys(tree) == [1, 2]
    tree.finger_insert(3, "")
    assert pre_order_keys(tree) == [2, 1, 3]


def test_single_right_rotation_finger() -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert pre_order_keys(tree) == []
    tree.finger_insert(3, "")
    assert pre_order_keys(tree) == [3]
    tree.finger_insert(2, "")
    assert pre_order_keys(tree) == [3, 2]
    tree.finger_insert(1, "")
    assert pre_order_keys(tree) == [2, 1, 3]


def test_double_right_rebalancing_finger() -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert pre_order_keys(tree) == []
    tree.finger_insert(1, "")
    assert pre_order_keys(tree) == [1]
    tree.finger_insert(3, "")
    assert pre_order_keys(tree) == [1, 3]
    tree.finger_insert(2, "")
    assert pre_order_keys(tree) == [2, 1, 3]


def test_double_left_rebalancing_finger() -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert pre_order_keys(tree) == []
    tree.finger_insert(3, "")
    assert pre_order_keys(tree) == [3]
    tree.finger_insert(1, "")
    assert pre_order_keys(tree) == [3, 1]
    tree.finger_insert(2, "")
    assert pre_order_keys(tree) == [2, 1, 3]


def test_delete(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    basic_tree_insert.delete(root.left.left)
    assert pre_order_keys(basic_tree_insert) == [8, 4, 6, 15, 11, 54]
    assert (root := basic_tree_insert.get_root()) is not None
    assert root.left.height == 1

    basic_tree_insert.delete(root.left)
    assert pre_order_keys(basic_tree_insert) == [8, 6, 15, 11, 54]
    assert (root := basic_tree_insert.get_root()) is not None
    assert root.left.height == 0

    basic_tree_insert.delete(root.right)
    assert pre_order_keys(basic_tree_insert) == [8, 6, 54, 11]
    assert (root := basic_tree_insert.get_root()) is not None
    assert root.left.height == 0


def test_delete_left(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    basic_tree_insert.delete(root.left)
    assert pre_order_keys(basic_tree_insert) == [8, 6, 3, 15, 11, 54]
    assert (root := basic_tree_insert.get_root()) is not None
    assert root.left.height == 1


def test_delete_right(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    basic_tree_insert.delete(root.right)
    assert pre_order_keys(basic_tree_insert) == [8, 4, 3, 6, 54, 11]
    assert (root := basic_tree_insert.get_root()) is not None
    assert root.right.height == 1


def test_delete_root(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    basic_tree_insert.delete(root)
    assert (root := basic_tree_insert.get_root()) is not None
    assert root.key == 11
    assert pre_order_keys(basic_tree_insert) == [11, 4, 3, 6, 15, 54]
    assert root.height == 2
    assert root.left.height == 1
    assert root.right.right.height == 0
    assert root.right.height == 1


def test_right_join(basic_tree_insert: AVLTreeProtocol) -> None:
    tree2: AVLTreeProtocol = AVLTree()
    tree2.insert(56, "")
    basic_tree_insert.join(tree2, 55, "")
    assert pre_order_keys(basic_tree_insert) == [8, 4, 3, 6, 15, 11, 55, 54, 56]


def test_left_join(basic_tree_insert: AVLTreeProtocol) -> None:
    tree2: AVLTreeProtocol = AVLTree()
    tree2.insert(0, "")
    basic_tree_insert.join(tree2, 1, "")
    assert pre_order_keys(basic_tree_insert) == [8, 4, 1, 0, 3, 6, 15, 11, 54]


def test_empty_join_with_empty() -> None:
    tree1: AVLTreeProtocol = AVLTree()
    tree2: AVLTreeProtocol = AVLTree()
    
    tree1.join(tree2, 1, "")
    assert pre_order_keys(tree1) == [1]
    assert tree1.size() == 1


def test_join_with_empty() -> None:
    tree1: AVLTreeProtocol = AVLTree()
    tree2: AVLTreeProtocol = AVLTree()
    tree1.insert(2, "")
    
    tree1.join(tree2, 1, "")
    assert pre_order_keys(tree1) == [2, 1]
    assert tree1.size() == 2


def test_empty_join_with_not_empry() -> None:
    tree1: AVLTreeProtocol = AVLTree()
    tree2: AVLTreeProtocol = AVLTree()
    tree2.insert(2, "")
    
    tree1.join(tree2, 1, "")
    assert pre_order_keys(tree1) == [2, 1]
    assert tree1.size() == 2


def test_split_root(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    (left, right) = basic_tree_insert.split(root)
    assert pre_order_keys(left) == [4, 3, 6]
    assert pre_order_keys(right) == [15, 11, 54]


def test_split_right_side_leaf(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    (left, right) = basic_tree_insert.split(root.right.left)
    assert pre_order_keys(left) == [4, 3, 6, 8]
    assert pre_order_keys(right) == [54, 15]


def test_split_left_side_leaf(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    (left, right) = basic_tree_insert.split(root.left.right)
    assert pre_order_keys(left) == [3, 4]
    assert pre_order_keys(right) == [15, 11, 8, 54]


def test_split_left_side_middle_node(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    (left, right) = basic_tree_insert.split(root.left)
    assert pre_order_keys(left) == [3]
    assert pre_order_keys(right) == [15, 8, 6, 11, 54]


def test_split_right_side_middle_node(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    (left, right) = basic_tree_insert.split(root.right)
    assert pre_order_keys(left) == [4, 3, 8, 6, 11]
    assert pre_order_keys(right) == [54]


def test_split_no_left(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    (left, right) = basic_tree_insert.split(root.left.left)
    assert pre_order_keys(left) == []
    assert pre_order_keys(right) == [8, 6, 4, 15, 11, 54]


def test_split_no_right(basic_tree_insert: AVLTreeProtocol) -> None:
    assert (root := basic_tree_insert.get_root()) is not None
    (left, right) = basic_tree_insert.split(root.right.right)
    assert pre_order_keys(left) == [8, 4, 3, 6, 11, 15]
    assert pre_order_keys(right) == []


def test_split_single_node() -> None:
    one_node_tree: AVLTreeProtocol = AVLTree()
    one_node_tree.insert(2, "")
    assert (root := one_node_tree.get_root()) is not None
    (left, right) = one_node_tree.split(root)
    assert pre_order_keys(left) == []
    assert pre_order_keys(right) == []


def test_split_big_tree() -> None:
    tree: AVLTreeProtocol = AVLTree()
    tree.insert(10, "")
    tree.insert(5, "")
    tree.insert(20, "")
    tree.insert(2, "")
    tree.insert(7, "")
    tree.insert(15, "")
    tree.insert(30, "")
    tree.insert(1, "")
    tree.insert(3, "")
    tree.insert(6, "")
    node_key_8, _, _ = tree.insert(8, "")
    tree.insert(17, "")
    tree.insert(9, "")
    assert pre_order_keys(tree) == [10, 5, 2, 1, 3, 7, 6, 8, 9, 20, 15, 17, 30]

    (left, right) = tree.split(node_key_8)
    assert left.search(8)[0] == None
    assert right.search(8)[0] == None
    assert pre_order_keys(left) == [5, 2, 1, 3, 6, 7]
    assert pre_order_keys(right) == [15, 10, 9, 20, 17, 30]


def test_avl_to_array(basic_tree_insert: AVLTreeProtocol) -> None:
    assert basic_tree_insert.avl_to_array() == [
        (3, "3"),
        (4, "4"),
        (6, "6"),
        (8, "8"),
        (11, "11"),
        (15, "15"),
        (54, "54"),
    ]


def test_size(basic_tree_insert: AVLTreeProtocol) -> None:
    tree: AVLTreeProtocol = AVLTree()
    assert tree.size() == 0
    tree.insert(-5, "")
    assert tree.size() == 1
    tree.insert(-10, "")
    assert tree.size() == 2
    tree.insert(-6, "")
    tree.insert(-15, "")
    tree.insert(-20, "")
    tree.insert(-3, "")
    tree.finger_insert(-4, "")
    tree.finger_insert(-11, "")
    tree.finger_insert(-1, "")
    assert tree.size() == 9
    tree.join(basic_tree_insert, 0, "")
    assert tree.size() == 17


def print_tree(node=None, level=0, prefix="Root: ") -> None:
    if node is not None:
        print(" " * (level * 4) + prefix + f"({node.key})")
        if node.left or node.right:
            if node.left:
                print_tree(node.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            if node.right:
                print_tree(node.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")
    else:
        print(" " * (level * 4) + prefix + "None")
