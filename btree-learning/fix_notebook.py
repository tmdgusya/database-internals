#!/usr/bin/env python3
import json

with open('/home/roach/database-internals/btree-learning/btree_study.nblr', 'r') as f:
    nb = json.load(f)

# 인트로 셀 내용
intro_source = """# 🌳 B-Tree 수학적 이해 인터랙티브 학습

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

**관찰 포인트**: B-Tree는 훨씬 "납작(flat)"하다!"""

intro_cell = {
    "cell_type": "markdown",
    "source": intro_source,
    "outputs": [],
    "execution_count": None
}

# 인트로 셀 추가
nb['cells'].insert(0, intro_cell)

# 중복 셀 제거 (셀 4와 5가 동일한지 확인 후 제거)
if len(nb['cells']) > 6:
    cell_4_source = nb['cells'][4]['source'][:50]
    cell_5_source = nb['cells'][5]['source'][:50]
    if cell_4_source == cell_5_source:
        nb['cells'].pop(5)
        print("✅ 중복 셀 제거됨")

# 저장
with open('/home/roach/database-internals/btree-learning/btree_study.nblr', 'w') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print('✅ 수정 완료!')
print(f'   총 셀 수: {len(nb["cells"])}')
print()
print('📋 최종 셀 목록:')
for i, cell in enumerate(nb['cells']):
    t = cell['cell_type']
    s = cell['source'][:40].replace('\n', ' ')
    print(f'  {i+1:2}. [{t:8}] {s}...')
