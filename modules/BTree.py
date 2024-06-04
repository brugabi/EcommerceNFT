class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Grau mínimo
        self.leaf = leaf  # True se o nó é folha
        self.keys = []  # Lista de chaves
        self.children = []  # Lista de filhos

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t
    
    def traverse(self):
        return self._traverse(self.root)
    
    def _traverse(self, node):
        records = []
        for i in range(len(node.keys)):
            if not node.leaf:
                records.extend(self._traverse(node.children[i]))
            records.append(node.keys[i])
        if not node.leaf:
            records.extend(self._traverse(node.children[len(node.keys)]))
        return records
    
    def search(self, k):
        return self._search(self.root, k)
    
    def _search(self, node, k):
        i = 0
        while i < len(node.keys) and k > node.keys[i][0]:
            i += 1
        if i < len(node.keys) and k == node.keys[i][0]:
            return node.keys[i]
        if node.leaf:
            return None
        return self._search(node.children[i], k)
    
    def insert(self, k):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            temp = BTreeNode(self.t)
            self.root = temp
            temp.children.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, k)
        else:
            self._insert_non_full(root, k)
    
    def _insert_non_full(self, node, k):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append((None, None))
            while i >= 0 and k[0] < node.keys[i][0]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            while i >= 0 and k[0] < node.keys[i][0]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if k[0] > node.keys[i][0]:
                    i += 1
            self._insert_non_full(node.children[i], k)
    
    def _split_child(self, node, i):
        t = self.t
        y = node.children[i]
        z = BTreeNode(t, y.leaf)
        node.children.insert(i + 1, z)
        node.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:(2 * t - 1)]
        y.keys = y.keys[0:(t - 1)]
        if not y.leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]
    
    def filter_records(self, min_value=None, max_value=None, substring=None):
        all_records = self.traverse()
        filtered_records = []

        for record in all_records:
            key, value = record
            if min_value is not None and value['valor'] < min_value:
                continue
            if max_value is not None and value['valor'] > max_value:
                continue
            if substring is not None and substring.lower() not in value['nome'].lower():
                continue
            filtered_records.append(record)

        return filtered_records