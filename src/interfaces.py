from typing import Optional, Protocol, Self
from src.AVLTree import AVLNode


class AVLNodeProtocol(Protocol):

    key: Optional[int]
    value: str
    left: AVLNode
    right: AVLNode
    parent: AVLNode
    height: int

    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key: int, value: str) -> None: ...

    """returns whether self is not a virtual node

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""

    def is_real_node(self) -> bool: ...


"""
A class implementing an AVL tree.
"""


class AVLTreeProtocol(Protocol):
    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """

    def search(self, key: int) -> tuple[Optional[AVLNode], int]: ...

    """searches for a node in the dictionary corresponding to the key, starting at the max

	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""

    def finger_search(self, key: int) -> tuple[Optional[AVLNode], int]: ...

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""

    def insert(self, key: int, val: str) -> tuple[AVLNode, int, int]: ...

    """inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""

    def finger_insert(self, key: int, val: str) -> tuple[AVLNode, int, int]: ...

    """deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""

    def delete(self, node: AVLNode) -> None: ...

    """joins self with item and another AVLTree

	@type tree2: AVLTree
	@param tree2: a dictionary to be joined with self
	@type key: int
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""

    def join(self, tree2: Self, key: int, val: str) -> None: ...

    """splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the
	dictionary larger than node.key.
	"""

    def split(self, node: AVLNode) -> tuple[Self, Self]: ...

    """returns an array representing dictionary

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""

    def avl_to_array(self) -> list[tuple[int, str]]: ...

    """returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""

    def max_node(self) -> Optional[AVLNode]: ...

    """returns the number of items in dictionary

	@rtype: int
	@returns: the number of items in dictionary
	"""

    def size(self) -> int: ...

    """returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""

    def get_root(self) -> Optional[AVLNode]: ...
