# Boundary Convergence Engine과 Dynamics Engine 연계

**작성일**: 2026-02-02  
**목적**: Boundary Convergence Engine과 Dynamics Engine의 통합 사용법

---

## 🔗 두 엔진의 관계

### Dynamics Engine (8번)
- **역할**: 인지 동역학 계산
- **출력**: 엔트로피, 코어 강도, 회전 토크
- **위치**: [Dynamics Engine](https://pypi.org/project/dynamics-engine/)

### Boundary Convergence Engine (9번)
- **역할**: 경계-공간 정합 동역학
- **출력**: 수렴 과정, 밀도 맵, 경계 형성
- **위치**: 현재 엔진

---

## 🔄 통합 구조

```
┌─────────────────────────────────────┐
│   Cognitive Kernel                  │
│                                      │
│  ┌──────────────────────────────┐  │
│  │ Dynamics Engine (8번)         │  │
│  │ - Entropy 계산                │  │
│  │ - Core Strength 계산          │  │
│  │ - Rotational Torque 생성      │  │
│  └───────────┬──────────────────┘  │
│              │                       │
│              ↓                       │
│  ┌──────────────────────────────┐  │
│  │ Boundary Convergence (9번)   │  │
│  │ - 경계 생성                  │  │
│  │ - 밀도 추정                  │  │
│  │ - 수렴 동역학                │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## 💡 통합 사용 예제

### 예제 1: Core Strength를 경계 반지름으로 사용

```python
from dynamics_engine import DynamicsEngine, DynamicsConfig
from boundary_convergence_engine import (
    BoundaryConvergenceEngine,
    BoundaryConvergenceConfig,
    Point
)

# Dynamics Engine으로 코어 강도 계산
dynamics = DynamicsEngine()
memories = [...]  # 기억 리스트
core_strength = dynamics.calculate_core_strength(memories)

# Boundary Convergence Engine 설정
# 코어 강도를 경계 반지름으로 사용
boundary_config = BoundaryConvergenceConfig(
    boundary_radius=core_strength,  # 동적 반지름
    initial_boundary_points=8,
    max_iterations=1000
)

boundary_engine = BoundaryConvergenceEngine(boundary_config)
result = boundary_engine.converge()
```

### 예제 2: Memory Importance를 밀도로 변환

```python
from memoryrank_engine import MemoryRankEngine

# MemoryRank Engine으로 중요도 계산
memoryrank = MemoryRankEngine()
top_memories = memoryrank.get_top_memories(k=100)

# 중요도를 밀도 가중치로 변환
importance_weights = {}
for memory in top_memories:
    # 기억의 좌표를 Point로 변환
    point = Point(memory.x, memory.y)
    importance_weights[point] = memory.importance

# Boundary Convergence Engine으로 수렴
result = boundary_engine.converge(importance_weights=importance_weights)
```

### 예제 3: Precession Phi를 위상으로 사용

```python
# Dynamics Engine의 precession_phi를 위상 공간 샘플링으로 활용
precession_phi = dynamics.state.precession_phi

# 위상에 따라 경계 점 개수 조절
n_points = int(precession_phi * 100) % 1000 + 4

boundary_config = BoundaryConvergenceConfig(
    initial_boundary_points=n_points,
    boundary_radius=core_strength
)

boundary_engine = BoundaryConvergenceEngine(boundary_config)
result = boundary_engine.converge()
```

---

## 🧠 인지 모델링 통합

### 완전한 인지 공간 형성

```python
# 1. Dynamics Engine: 인지 동역학 계산
entropy = dynamics.calculate_entropy(probabilities)
core_strength = dynamics.calculate_core_strength(memories)
torque = dynamics.generate_torque(options, entropy, mode)

# 2. Boundary Convergence Engine: 경계 형성
boundary_config = BoundaryConvergenceConfig(
    boundary_radius=core_strength,
    initial_boundary_points=int(entropy * 10) + 4
)
boundary_engine = BoundaryConvergenceEngine(boundary_config)

# 3. 기억의 중요도를 밀도로 변환
importance_weights = {
    Point(m.x, m.y): m.importance
    for m in memories
}

# 4. 수렴 실행
result = boundary_engine.converge(importance_weights=importance_weights)

# 5. 인지 공간의 실체 확인
print(f"인지 공간 밀도: {result.get_latest_state().density:.4f}")
print(f"경계 안정성: {1.0 - result.mismatch:.4f}")
```

---

## 📊 데이터 흐름

```
Memories (Panorama Memory Engine)
    ↓
MemoryRank Engine → Importance Scores
    ↓
Dynamics Engine → Core Strength, Entropy
    ↓
Boundary Convergence Engine → Boundary Formation
    ↓
Cognitive Space Entity
```

---

## 🔬 물리적 의미

### Core Strength → Boundary Radius
- **의미**: 인지의 중력이 경계의 크기를 결정
- **물리**: 코어 강도가 클수록 큰 경계 형성

### Memory Importance → Density
- **의미**: 중요한 기억이 밀도 높은 영역 형성
- **물리**: 밀도가 높을수록 경계가 안정화

### Precession Phi → Phase Sampling
- **의미**: 위상 회전이 경계 점 분포 결정
- **물리**: 위상이 변하면 경계가 재형성

---

## 📝 참고 문서

- [Dynamics Engine README](https://pypi.org/project/dynamics-engine/)
- [Space Filling Dynamics](../../Cognitive_Kernel/docs/SPACE_FILLING_DYNAMICS.md)
- [Boundary Convergence Engine Design](../../Cognitive_Kernel/docs/BOUNDARY_CONVERGENCE_ENGINE_DESIGN.md)

---

**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0

