#!/usr/bin/env python3
import json

notebook = {
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 4,
    'cells': []
}

cells = []

# Cell 1: Introduction
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': '''# 🌳 B-Tree 수학적 이해 인터랙티브 학습

> **학습 목표**: 직관적 감각에서 수학적 증명까지, B-Tree의 효율성을 단계적으로 이해하기

## 📊 학습 로드맵

```
[단계 1]        [단계 2]        [단계 3]        [단계 4]
직관적 감각  →  구체적 수치  →  패턴 인식  →  수학적 형식화
   ↓              ↓              ↓              ↓
"왜 효율적?"   "숫자로       "규칙을        "증명으로
              확인하기"     일반화하기"    표현하기"
```

---

## 1. B-Tree란 무엇인가?

### 직관적 이해
B-Tree는 **디스크와 같은 외부 저장장치**에서 데이터를 효율적으로 관리하기 위한 균형 탐색 트리입니다.

**핵심 아이디어**: 한 노드에 여러 키를 저장하여 디스크 I/O를 최소화한다!

### 시각적 비교: B-Tree vs 이진 트리

```
[이진 트리 - 높이 3-4]          [B-Tree(t=3) - 높이 2]

        50                           [30, 60, 90]
       /  \\                          /    |    \\
     30    80               [10,20] [40,50] [70,80] [100]
    / \\    / \\
  20  40  70  90
  /       /
10      60
```

**관찰 포인트**: B-Tree는 훨씬 "납작(flat)"하다!'''
})

# Cell 2: Mathematical Definition
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': '''## 2. B-Tree의 수학적 정의

### 차수(order)가 $t$인 B-Tree

B-Tree $T$는 다음 **5가지 성질**을 만족하는 균형 탐색 트리입니다:

| 성질 | 수학적 표현 | 의미 |
|------|-------------|------|
| **(1) 노드 키 개수 범위** | $t-1 \\leq |keys| \\leq 2t-1$ | 각 노드는 최소 $t-1$개, 최대 $2t-1$개의 키를 가진다 |
| **(2) 루트 특수 규칙** | $1 \\leq |keys|_{root} \\leq 2t-1$ | 루트는 최소 1개의 키를 가진다 |
| **(3) 자식 수 관계** | $|children| = |keys| + 1$ | $k$개의 키를 가진 노드는 $k+1$개의 자식을 가진다 |
| **(4) 키 순서** | $k_1 < k_2 < ... < k_m$ | 노드 내 키는 오름차순으로 정렬 |
| **(5) 균형 성질** | $\\forall$ leaf: $depth(leaf) = h$ | 모든 리프 노드는 같은 깊이 $h$에 있다 |

### 예시: t=3인 B-Tree (2-3-4 Tree)

```
┌─────────────────────────────────────────┐
│  최소 키: t-1 = 2개                    │
│  최대 키: 2t-1 = 5개                   │
│  최소 자식: t = 3개                    │
│  최대 자식: 2t = 6개                   │
└─────────────────────────────────────────┘
```

### 왜 $t-1$과 $2t-1$인가?
- **최소 $t-1$개**: 노드가 너무 비어있지 않도록 보장 (공간 효율성)
- **최대 $2t-1$개**: 노드가 꽉 차면 분할(split) 발생 → 트리 성장'''
})

# Cell 3: Python Code - Properties
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': '''# 실습 1: t값에 따른 B-Tree 속성 계산

def btree_properties(t):
    """
    주어진 t값에 따른 B-Tree 속성을 계산합니다.
    """
    min_keys_non_root = t - 1
    max_keys = 2 * t - 1
    min_children = t
    max_children = 2 * t

    return {
        't': t,
        'min_keys_non_root': min_keys_non_root,
        'max_keys': max_keys,
        'min_children': min_children,
        'max_children': max_children
    }

# 다양한 t값에 대해 계산
print("=" * 70)
print("📊 t값에 따른 B-Tree 속성 비교")
print("=" * 70)
print(f"{'t값':<8} {'최소 키':<12} {'최대 키':<12} {'최소 자식':<12} {'최대 자식':<12}")
print("-" * 70)

for t in [2, 3, 4, 10, 100]:
    props = btree_properties(t)
    print(f"t={t:<4} {props['min_keys_non_root']:<12} {props['max_keys']:<12} "
          f"{props['min_children']:<12} {props['max_children']:<12}")

print("=" * 70)''',
    'outputs': []
})

# Cell 4: Height Analysis
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': '''## 3. B-Tree 높이 분석

### 직관적 이해: 왜 높이가 로그 시간인가?

**핵심 통찰**: B-Tree는 각 레벨에서 "최소 $t$배"씩 분기한다!

```
레벨 0 (루트):     최소 1개 노드
레벨 1:            최소 t개 노드
레벨 2:            최소 t²개 노드
레벨 h:            최소 t^h개 노드 (리프)
```

> 각 레벨마다 최소 $t$배씩 늘어나므로, $n$개의 키를 저장하려면 높이가 로그 시간이 된다.

### 수학적 정리: B-Tree의 높이 상한

$n$개의 키를 저장하는 차수 $t$의 B-Tree의 높이 $h$는 다음을 만족한다:

$$h \\leq \\log_t \\frac{n+1}{2}$$

#### 증명 과정:

**Step 1**: 높이 $h$인 B-Tree의 최소 키 수는 $2t^h - 1$

**Step 2**: $n$개의 키를 저장하려면:
$$n \\geq 2t^h - 1$$

**Step 3**: $h$에 대해 정리:
$$h \\leq \\log_t\\frac{n+1}{2}$$'''
})

# Cell 5: Height Calculation Code
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': '''import math

def btree_max_height(n, t):
    """
    n개의 키를 가진 B-Tree(t)의 최대 높이를 계산합니다.
    공식: h <= log_t((n+1)/2)
    """
    if n <= 0:
        return 0
    return math.ceil(math.log((n + 1) / 2, t))

def btree_min_keys_for_height(h, t):
    """
    높이 h인 B-Tree(t)의 최소 키 수를 계산합니다.
    공식: n_min = 2*t^h - 1
    """
    return 2 * (t ** h) - 1

# 예시: 다양한 n과 t에 대해 계산
print("📊 B-Tree 높이 분석")
print("=" * 70)

# 예시 1: n=100, t=3
n, t = 100, 3
print(f"\\n📌 예시 1: n={n}개 키, t={t}")
print(f"   최대 높이: {btree_max_height(n, t)}")
print(f"   높이 3까지 저장 가능한 최소 키 수: {btree_min_keys_for_height(3, t)}")

# 예시 2: 대규모 데이터
print(f"\\n📌 예시 2: 대규모 데이터 (n=1,000,000)")
n = 1_000_000
for t in [10, 100, 1000]:
    h = btree_max_height(n, t)
    print(f"   t={t:4}: 최대 높이 = {h}")

print("\\n" + "=" * 70)''',
    'outputs': []
})

# Cell 6: Comparison with BST
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': '''## 4. B-Tree vs 이진 탐색 트리 비교

### 높이 비교 (n=1,000,000)

| 자료구조 | 높이 공식 | 예상 높이 |
|:---|:---|:---:|
| BST (최악) | $h = n - 1$ | 999,999 |
| BST (평균) | $h \\approx 1.39 \\log_2 n$ | ~28 |
| AVL/Red-Black | $h \\leq 1.44 \\log_2(n+2)$ | ~29 |
| B-Tree (t=100) | $h \\leq \\log_{100}((n+1)/2)$ | **3** |
| B-Tree (t=1000) | $h \\leq \\log_{1000}((n+1)/2)$ | **2** |

### 디스크 접근 관점

디스크 접근 1회 = 10ms (가정) 시:

| 자료구조 | 높이 | 총 접근 시간 |
|:---|:---:|:---:|
| AVL Tree | ~29 | 290ms |
| B-Tree (t=100) | 3 | 30ms |
| **개선율** | | **~90% 감소** |'''
})

# Cell 7: B-Tree Implementation
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': '''# B-Tree 기본 구현

class BTreeNode:
    def __init__(self, t, leaf=True):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.children = []

    def is_full(self):
        return len(self.keys) >= 2 * self.t - 1

    def __repr__(self):
        return f"Node(keys={self.keys}, leaf={self.leaf})"

class BTree:
    def __init__(self, t):
        self.t = t
        self.root = BTreeNode(t)

    def insert(self, key):
        if self.root.is_full():
            new_root = BTreeNode(self.t, leaf=False)
            new_root.children.append(self.root)
            self.split_child(new_root, 0)
            self.root = new_root
        self.insert_non_full(self.root, key)

    def split_child(self, parent, i):
        t = self.t
        full_child = parent.children[i]
        new_child = BTreeNode(t, full_child.leaf)

        mid = t - 1
        parent.keys.insert(i, full_child.keys[mid])
        parent.children.insert(i + 1, new_child)

        new_child.keys = full_child.keys[mid + 1:]
        full_child.keys = full_child.keys[:mid]

        if not full_child.leaf:
            new_child.children = full_child.children[mid + 1:]
            full_child.children = full_child.children[:mid + 1]

    def insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if node.children[i].is_full():
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self.insert_non_full(node.children[i], key)

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node.leaf:
            return 0
        return 1 + self._height(node.children[0])

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return True
        if node.leaf:
            return False
        return self._search(node.children[i], key)

    def count_nodes(self):
        return self._count_nodes(self.root)

    def _count_nodes(self, node):
        count = 1
        if not node.leaf:
            for child in node.children:
                count += self._count_nodes(child)
        return count

# 실습: B-Tree 생성 및 테스트
print("🧪 B-Tree 실습")
print("=" * 50)

for t in [2, 3, 4]:
    print(f"\\n📌 t={t}인 B-Tree에 1~20 삽입:")
    btree = BTree(t)
    for key in range(1, 21):
        btree.insert(key)

    print(f"   높이: {btree.height()}")
    print(f"   총 노드 수: {btree.count_nodes()}")
    print(f"   루트: {btree.root}")
    print(f"   키 15 검색: {btree.search(15)}")
    print(f"   키 100 검색: {btree.search(100)}")''',
    'outputs': []
})

# Cell 8: Visualization
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': '''# B-Tree 시각화 함수

def visualize_btree(node, prefix="", is_last=True):
    """
    텍스트 기반 B-Tree 시각화
    """
    result = []
    connector = "└── " if is_last else "├── "
    result.append(f"{prefix}{connector}{node.keys}")

    if not node.leaf:
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            result.extend(visualize_btree(child, new_prefix, is_last_child))

    return result

def print_btree(btree):
    print(f"\\n📊 B-Tree (t={btree.t}, 높이={btree.height()}):")
    lines = visualize_btree(btree.root)
    for line in lines:
        print(line)

# t=3 B-Tree 시각화
btree = BTree(3)
for key in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
    btree.insert(key)

print_btree(btree)''',
    'outputs': []
})

# Cell 9: Practice Problems
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': '''## 5. 실습 과제

### 과제 1: t값에 따른 트리 높이 변화

1000개의 키를 저장할 때, t값에 따른 B-Tree의 최대 높이를 계산하시오.

| t값 | 최대 높이 |
|:---:|:---:|
| t=2 | ? |
| t=10 | ? |
| t=100 | ? |
| t=1000 | ? |

### 과제 2: 디스크 접근 횟수 계산

다음 조건에서 단일 키 탐색 시 디스크 접근 횟수를 계산하시오:
- 테이블 크기: 1억 개 레코드
- 디스크 블록 크기: 8KB
- 키 크기: 16바이트
- 포인터 크기: 8바이트

### 과제 3: B-Tree vs B+Tree

B+Tree가 B-Tree보다 범위 쿼리(range query)에서 더 효율적인 이유를 설명하시오.'''
})

# Cell 10: Practice Code Template
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': '''# 과제 1: t값에 따른 트리 높이 변화 계산

print("📚 과제 1: t값에 따른 트리 높이 변화 (n=1000)")
print("=" * 50)

n = 1000
for t in [2, 10, 100, 1000]:
    h = btree_max_height(n, t)
    print(f"t={t:4}: 최대 높이 = {h}")

print("\\n" + "=" * 50)

# 과제 2: 디스크 접근 횟수 계산
print("\\n📚 과제 2: 디스크 접근 횟수 계산")
print("=" * 50)

def calculate_t(block_size, key_size, pointer_size):
    """
    디스크 블록 크기와 키/포인터 크기로부터 t값 계산
    """
    entry_size = key_size + pointer_size
    t = int(block_size / (2 * entry_size))
    return t

# 조건
block_size = 8192  # 8KB
key_size = 16      # 16 bytes
pointer_size = 8   # 8 bytes
n = 100_000_000    # 1억 개

t = calculate_t(block_size, key_size, pointer_size)
h = btree_max_height(n, t)

print(f"블록 크기: {block_size} bytes")
print(f"키 크기: {key_size} bytes")
print(f"포인터 크기: {pointer_size} bytes")
print(f"테이블 크기: {n:,} 개")
print(f"\\n계산된 t값: {t}")
print(f"예상 최대 높이: {h}")
print(f"최악의 경우 디스크 접근: {h}회")''',
    'outputs': []
})

# Cell 11: Self Assessment
cells.append({
    'cell_type': 'markdown',
    'metadata': {},
    'source': '''## 6. 자가 진단 체크리스트

### 레벨 1: 직관적 이해 ⭐
- [ ] t값이 B-Tree 구조에 미치는 영향을 설명할 수 있다.
- [ ] 동일 데이터에서 t값에 따른 높이 변화를 예측할 수 있다.
- [ ] B-Tree와 이진 트리의 높이 차이를 수치적으로 비교할 수 있다.

### 레벨 2: 수치 검증 ⭐⭐
- [ ] 최대 높이 공식을 적용하여 구체적인 수치를 계산할 수 있다.
- [ ] 최소/최대 키 개수 범위를 계산할 수 있다.
- [ ] 분할 연산의 조건과 횟수를 분석할 수 있다.

### 레벨 3: 수식 유도 ⭐⭐⭐
- [ ] B-Tree 높이 상한 공식을 직접 유도할 수 있다.
- [ ] 키 개수와 노드 수의 관계식을 유도할 수 있다.
- [ ] 삽입 연산의 시간 복잡도를 엄밀하게 증명할 수 있다.

---

## 📖 참고 자료

1. **Introduction to Algorithms** (CLRS) - Chapter 18: B-Trees
2. **Database Management Systems** (Ramakrishnan & Gehrke) - Chapter 9: Tree-Structured Indexing
3. **The Art of Computer Programming** (Knuth) - Volume 3: Sorting and Searching

---

> **"수학은 단순히 계산하는 것이 아니라, 이해하는 것이다."**
>
> — B-Tree의 아름다움을 발견한 당신에게'''
})

# Cell 12: Advanced - B-Tree vs B+Tree
cells.append({
    'cell_type': 'code',
    'metadata': {},
    'source': '''# 추가 실습: B-Tree 성능 시뮬레이션

import random
import time

def simulate_search_performance(n, t, num_searches=1000):
    """
    B-Tree 검색 성능 시뮬레이션
    """
    btree = BTree(t)
    keys = list(range(1, n + 1))
    random.shuffle(keys)

    # 키 삽입
    for key in keys:
        btree.insert(key)

    # 검색 성능 측정
    search_keys = random.sample(keys, min(num_searches, n))

    # 높이 기반 접근 횟수 추정
    height = btree.height()
    disk_access_per_search = height + 1  # 루트부터 리프까지

    return {
        'n': n,
        't': t,
        'height': height,
        'nodes': btree.count_nodes(),
        'disk_access_per_search': disk_access_per_search,
        'total_disk_access_1000_searches': disk_access_per_search * 1000
    }

print("🔬 B-Tree 성능 시뮬레이션")
print("=" * 70)
print(f"{'n':<12} {'t':<8} {'높이':<8} {'노드 수':<12} {'1회 검색':<12} {'1000회 검색':<12}")
print("-" * 70)

scenarios = [
    (1000, 10),
    (10000, 50),
    (100000, 100),
    (1000000, 200),
]

for n, t in scenarios:
    result = simulate_search_performance(n, t, 100)
    print(f"{result['n']:<12,} {result['t']:<8} {result['height']:<8} "
          f"{result['nodes']:<12,} {result['disk_access_per_search']:<12} "
          f"{result['total_disk_access_1000_searches']:<12,}")

print("=" * 70)

# 분석
print("\\n📊 분석:")
print("- 테이블 크기가 1000배 증가해도 높이는 2배만 증가!")
print("- t값을 키우면 디스크 접근 횟수를 크게 줄일 수 있다.")
print("- 이것이 B-Tree가 데이터베이스 인덱스에 적합한 이유다.")''',
    'outputs': []
})

notebook['cells'] = cells

with open('/home/roach/database-internals/btree-learning/btree_interactive.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print('✅ B-Tree 인터랙티브 학습 노트북이 생성되었습니다!')
print('📁 파일 위치: /home/roach/database-internals/btree-learning/btree_interactive.ipynb')
