#id1: 328242284
#name1: nadav cherno
#username1: cherno
#id2:
#name2:
#username2:

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

    def is_real_node(self):
        """
        Determines if this node is a real node (not a virtual one).
        :return: True if real, False if virtual.
        """
        return self.key is not None


class AVLTree(object):
    def __init__(self):
        """
        Initializes an empty AVL tree.
        """
        self.root = None
        self.tree_size = 0  # Tracks the number of real nodes in the tree.

    def get_root(self):
        """
        Returns the root of the AVL tree.
        :return: The root node of the tree or None if the tree is empty.
        """
        return self.root

    def size(self):
        """
        Returns the number of nodes in the AVL tree.
        :return: Integer size of the tree.
        """
        return self.tree_size

    def search(self, key):
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
    def finger_search(self, key):
        """
        Searches for a node with the given key in the AVL tree.
        :param key: The key to search for.
        :return: A tuple (node, path_length):
            - node: The node with the matching key or None if not found.
            - path_length: Number of edges traversed during the search.
        """
        current_node = self.get_maximum()
        path_length = 0
        if not current_node:
            return None,path_length
        while key <= current_node.parent and current_node != self.root:
            if key == current_node.key:
                return current_node, path_length + 1
            elif key < current_node:
                current_node = current_node.parent
            path_length += 1
        while current_node and current_node.is_real_node():
            if key == current_node.key:
                return current_node, path_length + 1
            elif key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
            path_length += 1
        return None, path_length


    def insert(self, key, value):
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

        return new_node, path_length,promote

    def delete(self, node_to_remove):
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

        def replace_node_in_parent(old_node, new_node):
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
            node_to_remove = node_to_remove.left.left
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

    def convert_to_sorted_list(self):
        """
        Converts the AVL tree into a sorted list of (key, value) pairs.
        :return: A sorted list of tuples.
        """
        result = []

        def in_order_traversal(node):
            if node and node.is_real_node():
                in_order_traversal(node.left)
                result.append((node.key, node.value))
                in_order_traversal(node.right)

        in_order_traversal(self.root)
        return result

    def get_maximum(self):
        """
        Finds the node with the maximum key in the tree.
        :return: The node with the maximum key, or None if the tree is empty.
        """
        current_node = self.root
        while current_node and current_node.right and current_node.right.is_real_node():
            current_node = current_node.right
        return current_node

    # Internal helper methods
    def _rebalance_tree(self, node):
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

    def _rotate_left(self, node):
        """
        Performs a left rotation around the given node.
        """
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
        self._update_height(node)
        self._update_height(right)

    def _rotate_right(self, node):
        """
        Performs a right rotation around the given node.
        """
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
        self._update_height(node)
        self._update_height(left)

    def _update_height(self, node):
        """
        Updates the height of the given node.
        """
        if node and node.is_real_node():
            left_height = node.left.height if node.left else -1
            right_height = node.right.height if node.right else -1
            node.height = max(left_height, right_height) + 1


    def _get_balance_factor(self, node):
        """
        Calculates the balance factor of the given node.
        :return: The balance factor (left height - right height).
        """
        if not node or not node.is_real_node():
            return 0
        left_height = node.left.height if node.left.is_real_node() else -1
        right_height = node.right.height if node.right.is_real_node() else -1
        return left_height - right_height

    def _find_min(self, node):
        """
        Finds the minimum node starting from the given node.
        :return: The node with the smallest key in the subtree.
        """
        while node and node.left and node.left.is_real_node():
            node = node.left
        return node
