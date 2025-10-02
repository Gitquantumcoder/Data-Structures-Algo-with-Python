from typing import List, Tuple

class DSUWithRollback:
    def __init__(self, n: int) -> None:
        self.parent: List[int] = list(range(n))
        self.rank: List[int] = [1] * n
        self.history: List[Tuple[int, int, int]] = []  # (operation, x, previous_value)
        self.components: int = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            self.history.append(('noop', -1, -1))
            return
        if self.rank[x_root] < self.rank[y_root]:
            x_root, y_root = y_root, x_root
        self.history.append(('parent', y_root, self.parent[y_root]))
        self.parent[y_root] = x_root
        if self.rank[x_root] == self.rank[y_root]:
            self.history.append(('rank', x_root, self.rank[x_root]))
            self.rank[x_root] += 1
        self.components -= 1

    def rollback(self) -> None:
        while self.history:
            op, idx, prev = self.history.pop()
            if op == 'parent':
                self.parent[idx] = prev
                self.components += 1
            elif op == 'rank':
                self.rank[idx] = prev
            # skip 'noop'

# Usage: DSUWithRollback for edge changes and component queries
