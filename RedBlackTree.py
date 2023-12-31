from SweepData import SweepData

RED = True
BLACK = False

class Node:
  def __init__(self, key, data=None, color = RED):
    self.key = key
    self.data = data
    self.left = self.right = self.parent = NilNode.instance()
    self.color = color

class NilNode(Node):
  __instance__ = None

  @classmethod
  def instance(self):
    if self.__instance__ is None:
      self.__instance__ = NilNode()
    return self.__instance__

  def __init__(self):
    self.color = BLACK
    self.key = None
    self.left = self.right = self.parent = None

  def __bool__(self):
    return False

class RedBlackTree:
  def __init__(self):
    self.root = NilNode.instance()
    self.size = 0
    
  def __str__(self):
    return ("(root.size = %d)\n" % self.size)  + str(self.root)

  def is_empty(self):
    return not bool(self.root)

  def black_height(self, x = None):
    if x is None: x = self.root
    height = 0
    while x:
      x = x.left
      if not x or x.color == BLACK:
        height += 1
    return height

  def minimum(self, x = None):
    if x is None: x = self.root
    while x.left:
      x = x.left
    return x

  def maximum(self, x = None):
    if x is None: x = self.root
    while x.right:
      x = x.right
    return x

  def successor(self, x):
    if x.right:
      return self.minimum(x.right)
    y = x.parent
    while y and x == y.right:
      x = y
      y = y.parent
    return y

  def predecessor(self, x):
    if x.left:
        return self.maximum(x.left)
    y = x.parent
    while y and x == y.left:
      x = y
      y = y.parent
    return y

  def inorder(self, x = None):
    if x is None: x = self.root
    x = self.minimum()
    while x:
      yield x
      x = self.successor(x)
      
  def inorder_print(self, x = None):
    if x is None: x = self.root
    x = self.minimum()
    while x:
      print(x.key, x.data)
      x = self.successor(x)
    
  def search(self, key):
    x = self.root
    while x and x.key != key:
      if key < x.key:
        x = x.left
      else:
        x = x.right
    return x

  def sweep_search(self, key, event_x=None):
    x = self.root
    while x:
      adjusted_key = x.data.compute_adjusted_key(event_x)
      if key == adjusted_key:
        return x
      elif key < adjusted_key:
        x = x.left
      else:
        x = x.right
    return None
    
  def insert(self, key, data=None):
    x = Node(key, data)

    node = self.__insert_helper(x)

    x.color = RED
    while x != self.root and x.parent.color == RED:
      if x.parent == x.parent.parent.left:
        y = x.parent.parent.right
        if y and y.color == RED:
          x.parent.color = BLACK
          y.color = BLACK
          x.parent.parent.color = RED
          x = x.parent.parent
        else:
          if x == x.parent.right:
            x = x.parent
            self.__left_rotate(x)
          x.parent.color = BLACK
          x.parent.parent.color = RED
          self.__right_rotate(x.parent.parent)
      else:
        y = x.parent.parent.left
        if y and y.color == RED:
          x.parent.color = BLACK
          y.color = BLACK
          x.parent.parent.color = RED
          x = x.parent.parent
        else:
          if x == x.parent.left:
            x = x.parent
            self.__right_rotate(x)
          x.parent.color = BLACK
          x.parent.parent.color = RED
          self.__left_rotate(x.parent.parent)
    self.root.color = BLACK   
  
    return node
    
  def __insert_helper(self, z):

    y = NilNode.instance()
    x = self.root
    while x and x.key != z.key:
      y = x
      adjusted_key = x.data.compute_adjusted_key(z.data.segment[0][0]) 
      if z.key < adjusted_key:
        x = x.left
      else:
        x = x.right
        
    if z.key == y.key or z.key == x.key: return None
    
    z.parent = y
    if not y:
      self.root = z
    else:
      adjusted_key = y.data.compute_adjusted_key(z.data.segment[0][0])
      if z.key < adjusted_key:
        y.left = z
      else:
        y.right = z

    self.size += 1

    return z
    
# *** ---------------------------    

  def __left_rotate(self, x):
    if not x.right:
      raise "x.right is nil!"
    y = x.right
    x.right = y.left
    if y.left: y.left.parent = x
    y.parent = x.parent
    if not x.parent:
      self.root = y
    else:
      if x == x.parent.left:
        x.parent.left = y
      else:
        x.parent.right = y
    y.left = x
    x.parent = y

  def __right_rotate(self, x):
    if not x.left:
      raise "x.left is nil!"
    y = x.left
    x.left = y.right
    if y.right: y.right.parent = x
    y.parent = x.parent
    if not x.parent:
      self.root = y
    else:
      if x == x.parent.left:
        x.parent.left = y
      else:
        x.parent.right = y
    y.right = x
    x.parent = y

    
  def delete(self, z):
    if not z.left or not z.right:
      y = z
    else:
      y = self.successor(z)
    if not y.left:
      x = y.right
    else:
      x = y.left
    x.parent = y.parent

    if not y.parent:
      self.root = x
    else:
      if y == y.parent.left:
        y.parent.left = x
      else:
        y.parent.right = x

    if y != z: 
        z.key = y.key
        z.data = y.data

    if y.color == BLACK:
      self.__delete_fixup(x)

    self.size -= 1
    return y

  def __delete_fixup(self, x):
    while x != self.root and x.color == BLACK:
      if x == x.parent.left:
        w = x.parent.right
        if w.color == RED:
          w.color = BLACK
          x.parent.color = RED
          self.__left_rotate(x.parent)
          w = x.parent.right
        if w.left.color == BLACK and w.right.color == BLACK:
          w.color = RED
          x = x.parent
        else:
          if w.right.color == BLACK:
            w.left.color = BLACK
            w.color = RED
            self.__right_rotate(w)
            w = x.parent.right
          w.color = x.parent.color
          x.parent.color = BLACK
          w.right.color = BLACK
          self.__left_rotate(x.parent)
          x = self.root
      else:
        w = x.parent.left
        if w.color == RED:
          w.color = BLACK
          x.parent.color = RED
          self.__right_rotate(x.parent)
          w = x.parent.left
        if w.right.color == BLACK and w.left.color == BLACK:
          w.color = RED
          x = x.parent
        else:
          if w.left.color == BLACK:
            w.right.color = BLACK
            w.color = RED
            self.__left_rotate(w)
            w = x.parent.left
          w.color = x.parent.color
          x.parent.color = BLACK
          w.left.color = BLACK
          self.__right_rotate(x.parent)
          x = self.root
    x.color = BLACK

if __name__ == "__main__":
  tree = RedBlackTree()
  tree.insert_segment(0, SweepData([(0,0),(10,10)]))
  for node in tree.inorder():
    print(node.key, node.data.label)
  tree.insert_segment(9, SweepData([(1,9),(9,1)]))
  for node in tree.inorder():
    print(node.key, node.data.label)
  tree.insert_segment(7, SweepData([(2,7),(3,5)]))
  for node in tree.inorder():
    print(node.key, node.data.label)

