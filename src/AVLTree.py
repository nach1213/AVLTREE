#id1: 328242284
#name1: nadav cherno
#username1: cherno
#id2: 215713421
#name2: itamar nir
#username2: nirgottlieb
from typing import Protocol

import copy
class AVLNode(object):
    def __init__(self, key = None, value = None):
        """
        Represents a node in the AVL tree.
        :param key: The unique integer key for the node.
        :param value: The value associated with the key.
        """
        self.key = key
        self.value = value
        self.left = None if key is None else AVLNode()  # Left child node
        self.right = None if key is None else AVLNode() # Right child node
        self.parent = None  # Parent node
        self.height = 0 if key is not None else -1  # Height (-1 for virtual nodes)

    def is_real_node(self):#O(1)
        """
        Determines if this node is a real node (not a virtual one).
        :return: True if real, False if virtual.
        """
        return self.key is not None


class AVLTree(object):
    def __init__(self):#O(1)
        """
        Initializes an empty AVL tree.
        """
        self.max = AVLNode(None,None)
        self.root = None
        self.tree_size = 0  # Tracks the number of real nodes in the tree.

    def calculate_maximum(self):#O(log n)
        current_node = self.root
        while current_node and current_node.right and current_node.right.is_real_node():
            current_node = current_node.right
        return current_node

    def get_root(self):#O(1)
        """
        Returns the root of the AVL tree.
        :return: The root node of the tree or None if the tree is empty.
        """
        return self.root

    def size(self):#O(1)
        """
        Returns the number of nodes in the AVL tree.
        :return: Integer size of the tree.
        """
        return self.tree_size

    def search(self, key):#O(log n)
        """
        Searches for a node with the given key in the AVL tree.
        :param key: The key to search for.
        :return: A tuple (node, path_length):
            - node: The node with the matching key or None if not found.
            - path_length: Number of edges traversed during the search.
        """
        current_node = self.root
        path_length = 0
        while current_node and current_node.is_real_node():
            if key == current_node.key:
                return current_node, path_length+1
            elif key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
            path_length += 1
        return None, path_length
    def finger_search(self, key): #O(log n)
        """
        Searches for a node with the given key in the AVL tree.
        :param key: The key to search for.
        :return: A tuple (node, path_length):
            - node: The node with the matching key or None if not found.
            - path_length: Number of edges traversed during the search.
        """
        current_node = self.max_node()
        path_length = 0
        if not current_node or not  current_node.is_real_node():
            return None,path_length
        if key == current_node.key:
            return current_node, path_length + 1
        if not current_node.parent or not current_node.parent.is_real_node():
            return None, path_length
        while key <= current_node.parent.key and current_node != self.root:
            if key == current_node.key:
                return current_node, path_length + 1
            elif key < current_node.key:
                current_node = current_node.parent
            path_length += 1
            if not current_node.parent or not current_node.parent.is_real_node():
                break
        while current_node and current_node.is_real_node():
            if key == current_node.key:
                return current_node, path_length + 1
            elif key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
            path_length += 1
        return None, path_length


    def insert(self, key, value): # O(log n)
        """
        Inserts a new node into the AVL tree.
        :param key: The key for the new node (must be unique).
        :param value: The value associated with the key.
        :return: A tuple (node, path_length, rebalance_steps):
            - node: The newly inserted node.
            - path_length: Number of edges traversed during insertion.
            - rebalance_steps: Number of promote operations during rebalancing.
        """
        new_node = AVLNode(key, value)
        if self.root is None:
            self.root = new_node
            self.tree_size += 1
            return new_node, 0, 0

        current_node = self.root
        parent_node = None
        path_length = 0

        # Find the correct position for the new node
        while current_node and current_node.is_real_node():
            parent_node = current_node
            path_length += 1
            if key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right

        # Attach the new node to its parent
        new_node.parent = parent_node
        if key < parent_node.key:
            parent_node.left = new_node
        else:
            parent_node.right = new_node

        self.tree_size += 1
        promote= self._rebalance_tree(new_node)

        self.max = self.calculate_maximum()
        return new_node, path_length,promote

    def finger_insert(self, key, value): #O(log n)
        """
        Inserts a new node into the AVL tree.
        :param key: The key for the new node (must be unique).
        :param value: The value associated with the key.
        :return: A tuple (node, path_length, rebalance_steps):
            - node: The newly inserted node.
            - path_length: Number of edges traversed during insertion.
            - rebalance_steps: Number of promote operations during rebalancing.
        """
        new_node = AVLNode(key, value)
        if self.root is None:
            self.root = new_node
            self.max = new_node
            self.tree_size += 1
            return new_node, 0, 0

        current_node = self.max_node()
        path_length = 0
        parent_node = None
        while current_node != self.root and key <= current_node.parent.key:
            if key < current_node.key:
                current_node = current_node.parent
            path_length += 1
            if not current_node.parent or not current_node.parent.is_real_node():
                break
        while current_node and current_node.is_real_node():
            parent_node = current_node
            path_length += 1
            if key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        # Attach the new node to its parent
        new_node.parent = parent_node
        if key < parent_node.key:
            parent_node.left = new_node
        else:
            parent_node.right = new_node

        self.tree_size += 1
        promote = self._rebalance_tree(new_node)
        if self.max is None or new_node.key > self.max.key:
            self.max = new_node
        return new_node, path_length, promote

    def delete(self, node_to_remove): #O(log n)
        """
        Deletes a node from the AVL tree and maintains balance.
        :param node_to_remove: The node to delete.
        :return: None
        """
        if not node_to_remove or not node_to_remove.is_real_node():
            return
        if self.tree_size == 1:
            self.root = None
            self.tree_size = 0
            return

        def replace_node_in_parent(old_node, new_node): #O(log n)
            """
            Helper function to replace a node in the parent's child reference.
            """
            if not old_node.parent:
                self.root = new_node
            elif old_node == old_node.parent.left:
                old_node.parent.left = new_node
            else:
                old_node.parent.right = new_node
            if new_node:
                new_node.parent = old_node.parent

        if not node_to_remove.left.is_real_node() and not node_to_remove.right.is_real_node():
            if node_to_remove.parent.left == node_to_remove:
                node_to_remove.parent.left = AVLNode()
                return
            else:
                node_to_remove.parent.right = AVLNode()
        elif not node_to_remove.left.is_real_node():
            replace_node_in_parent(node_to_remove, node_to_remove.right)
        elif not node_to_remove.right.is_real_node():
            replace_node_in_parent(node_to_remove, node_to_remove.left)
        else:
            # Find the successor and swap values
            successor = self._find_min(node_to_remove.right)
            node_to_remove.key, node_to_remove.value = successor.key, successor.value
            self.delete(successor)
        self.tree_size -= 1
        self._rebalance_tree(node_to_remove.parent)
        self.max = self.calculate_maximum()

    def avl_to_array(self): #O(n)
        """
        Converts the AVL tree into a sorted list of (key, value) pairs.
        :return: A sorted list of tuples.
        """
        result = []

        def in_order_traversal(node):
            self._update_height(node)
            if node and node.is_real_node():
                in_order_traversal(node.left)
                result.append((node.key, node.value))
                in_order_traversal(node.right)

        in_order_traversal(self.root)
        return result

    def max_node(self):#O(1)
        """
                :return: The node with the maximum key, or None if the tree is empty.
                """
        return self.max


    # Internal helper methods
    def _rebalance_tree(self, node):#O(log n)
        """
        Rebalances the AVL tree starting from the given node upwards.
        :param node: The starting node for rebalancing.
        :return: The number of promote operations performed.
        """
        promote_count = 0
        while node:
            self._update_height(node)
            balance_factor = self._get_balance_factor(node)
            # Left-heavy
            if balance_factor > 1:
                if self._get_balance_factor(node.left) < 0:
                    self._rotate_left(node.left)
                self._rotate_right(node)
                promote_count += 1

            # Right-heavy
            elif balance_factor < -1:
                if self._get_balance_factor(node.right) > 0:
                    self._rotate_right(node.right)
                self._rotate_left(node)
                promote_count += 1
            node = node.parent
        return promote_count

    def _rotate_left(self, node,x=False):#O(1)
        """
        Performs a left rotation around the given node.
        """
        if node.key == self.root.key:
            x = True
        right = node.right
        node.right = right.left
        if right.left:
            right.left.parent = node
        right.parent = node.parent
        if not node.parent:
            self.root = right
        elif node == node.parent.left:
            node.parent.left = right
        else:
            node.parent.right = right
        right.left = node
        node.parent = right
        if x:
            self.root = right
        self._update_height(node)
        self._update_height(right)

    def _rotate_right(self, node, x = False):#O(1)
        """
        Performs a right rotation around the given node.
        """
        if node.key == self.root.key:
            x = True
        left = node.left
        node.left = left.right
        if left.right:
            left.right.parent = node
        left.parent = node.parent
        if not node.parent:
            self.root = left
        elif node == node.parent.right:
            node.parent.right = left
        else:
            node.parent.left = left
        left.right = node
        node.parent = left
        if x:
            self.root = left
        self._update_height(node)
        self._update_height(left)

    def _update_height(self, node):#O(1)
        """
        Updates the height of the given node.
        """
        if node and node.is_real_node():
            left_height = node.left.height if node.left else -1
            right_height = node.right.height if node.right else -1
            node.height = max(left_height, right_height) + 1


    def _get_balance_factor(self, node):#O(1)
        """
        Calculates the balance factor of the given node.
        :return: The balance factor (left height - right height).
        """
        if not node or not node.is_real_node():
            return 0
        left_height = node.left.height if node.left.is_real_node() else -1
        right_height = node.right.height if node.right.is_real_node() else -1
        return left_height - right_height

    def _find_min(self, node):#O(log n)
        """
        Finds the minimum node starting from the given node.
        :return: The node with the smallest key in the subtree.
        """
        while node and node.left and node.left.is_real_node():
            node = node.left
        return node

    def update_height_till_root(self,node):#O(log n)
        """
        Updates the height of the given node and all its ancestors.
        """
        while node:
            self._update_height(node)
            node = node.parent

    def join(self, second_tree, key, value):#O(log n)
        """
        Joins two AVL trees (self and second_tree) with a new node (key, value).
        Assumes all keys in 'self' are < key < all keys in 'second_tree'
        (or the symmetric case if reversed).
        """

        # Create bridging node
        x = AVLNode(key, value)

        # Case 1: second_tree is empty => just insert into self
        if second_tree.root is None or not second_tree.root.is_real_node():
            self.insert(key, value)
            return

        # Merge sizes
        self.tree_size += second_tree.tree_size + 1

        # Case 2: self is empty => insert into second_tree, then adopt its root
        if self.root is None or not self.root.is_real_node():
            second_tree.insert(key, value)
            self.root = second_tree.root
            return

        # Compare heights
        if second_tree.root.height <= self.root.height:
            # -----------------------------
            # self is taller (or same)
            # -----------------------------
            h = second_tree.root.height
            b = self.root
            p = None

            smaller = (b.key > x.key)

            # Descend self.root until height ~ h
            while b.is_real_node() and h < b.height:
                p = b
                if smaller:
                    b = b.left
                else:
                    b = b.right

            # Attach second_tree.root under x on one side, 'b' on the other
            if smaller:
                x.right = b
                x.left = second_tree.root
            else:
                x.left = b
                x.right = second_tree.root

            b.parent = x
            second_tree.root.parent = x

            # Insert bridging node x under p
            if p is None:
                # x becomes the new root
                self.root = x
                x.parent = None
            else:
                if smaller:
                    p.left = x
                else:
                    p.right = x
                x.parent = p

            # Update heights and rebalance
            self.update_height_till_root(b)
            self._rebalance_tree(x)

        else:
            # -----------------------------
            # second_tree is taller
            # -----------------------------
            # Temporarily set self.root to second_tree's root
            # so we effectively treat second_tree as "the base"
            self.root = second_tree.root

            h = self.root.height  # which is second_tree.root.height
            b = self.root
            p = None

            smaller = (b.key > x.key)

            # Descend second_tree.root until height ~ self's old root.height
            old_self_height = self.get_height(self.root_of_self_before_join) \
                if hasattr(self, "root_of_self_before_join") else (
                -1 if not self.root else self.root.height
            )
            # If you stored the old self height somewhere, or
            # just use your old tree's height logic.


            while b.is_real_node() and old_self_height < b.height:
                p = b
                if smaller:
                    b = b.left
                else:
                    b = b.right

            # If we ended on a virtual node, step back to its parent
            if b is not None and not b.is_real_node():
                b = b.parent

            # Attach bridging node x
            if smaller:
                x.right = b
            else:
                x.left = b

            # Fix parents
            b.parent = x
            if x.left is not None:
                x.left.parent = x
            if x.right is not None:
                x.right.parent = x

            if p is None:
                # x becomes new root
                self.root = x
                x.parent = None
            else:
                if smaller:
                    p.left = x
                else:
                    p.right = x
                x.parent = p

            self.update_height_till_root(b)
            self._rebalance_tree(x)
        self.max = self.calculate_maximum()

    def split(self,node):#O(log n)
        t_left = AVLTree()
        t_right = AVLTree()
        x_left = None
        x_right = None

        cur = self.root
        while True:
            if node.key <= cur.key:
                if x_right is None:
                    t_right.root = cur.right
                else:
                    sub_tree = AVLTree()
                    sub_tree.root = cur.right
                    t_right.join(sub_tree, x_right.key, x_right.value)
                x_right = cur
            if node.key >= cur.key:
                if x_left is None:
                    t_left.root = cur.left
                else:
                    sub_tree = AVLTree()
                    sub_tree.root = cur.left
                    t_left.join(sub_tree, x_left.key, x_left.value)
                x_left = cur
            if node.key == cur.key:
                break
            if node.key > cur.key:
                cur = cur.right
            else:
                cur = cur.left
        t_left.max = t_left.calculate_maximum()
        t_right.max = t_right.calculate_maximum()
        return (t_left,t_right)

