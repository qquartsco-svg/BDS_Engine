# Boundary Convergence Engine 사용 예제

**작성일**: 2026-02-02  
**엔진 번호**: 9번  
**버전**: 1.0.0

---

## 🚀 기본 사용법

### 예제 1: 기본 수렴 실행

```python
from boundary_convergence_engine import (
    BoundaryConvergenceEngine,
    BoundaryConvergenceConfig
)

# 기본 설정으로 엔진 생성
engine = BoundaryConvergenceEngine()

# 수렴 실행
result = engine.converge()

# 결과 확인
print(f"수렴 완료: {result.converged}")
print(f"반복 횟수: {result.iteration}")
print(f"경계 점 개수: {result.boundary_points}")
print(f"최종 불일치: {result.mismatch:.6f}")
print(f"경계 길이: {result.perimeter_estimate:.4f}")
print(f"면적: {result.area_estimate:.4f}")
```

### 예제 2: 커스텀 설정

```python
# 커스텀 설정
config = BoundaryConvergenceConfig(
    initial_boundary_points=8,  # 초기 8각형
    boundary_radius=2.0,  # 반지름 2.0
    max_iterations=500,  # 최대 500회 반복
    error_threshold=1e-8,  # 더 정밀한 수렴
    use_density_gradient=True,  # 밀도 기울기 사용
    use_mismatch_force=True  # mismatch 힘 사용
)

engine = BoundaryConvergenceEngine(config)
result = engine.converge()
```

### 예제 3: 중요도 가중치 사용

```python
from boundary_convergence_engine import Point

# 중요도 가중치 생성 (예: 기억의 중요도)
importance_weights = {
    Point(0.5, 0.5): 0.9,  # 중요한 기억
    Point(-0.3, 0.7): 0.7,
    Point(0.2, -0.4): 0.5,
    Point(-0.6, -0.2): 0.3,
}

# 가중치를 밀도로 변환하여 수렴
result = engine.converge(importance_weights=importance_weights)
```

---

## 🔬 수렴 과정 분석

### 예제 4: 수렴 히스토리 확인

```python
result = engine.converge()

# 수렴 과정 확인
for state in result.history:
    print(f"Iteration {state.iteration:3d}: "
          f"Points={state.boundary_points:4d}, "
          f"Mismatch={state.mismatch:.6f}, "
          f"Rate={state.convergence_rate:.2e}")
```

### 예제 5: 밀도 맵 확인

```python
result = engine.converge()

# 밀도 맵 확인
print(f"밀도 맵 크기: {len(result.density_map)}개 점")
for point, density in list(result.density_map.items())[:5]:
    print(f"  Point({point.x:.3f}, {point.y:.3f}): density={density:.4f}")
```

---

## 🏭 산업용 활용 예제

### 예제 6: 메시 생성 (FEM 전처리)

```python
# 고품질 메시 생성을 위한 설정
config = BoundaryConvergenceConfig(
    initial_boundary_points=16,
    max_iterations=2000,
    error_threshold=1e-9,
    density_resolution=200  # 고해상도
)

engine = BoundaryConvergenceEngine(config)
result = engine.converge()

# 경계 점을 메시 노드로 사용
mesh_nodes = [
    (state.perimeter_estimate / state.boundary_points, 
     state.area_estimate)
    for state in result.history
]
```

---

## 🔬 연구용 활용 예제

### 예제 7: 인지 공간 모델링

```python
# 기억의 중요도를 밀도로 변환
memory_importance = {
    Point(0.3, 0.4): 0.95,  # 매우 중요한 기억
    Point(-0.2, 0.5): 0.8,
    Point(0.1, -0.3): 0.6,
}

result = engine.converge(importance_weights=memory_importance)

# 인지 공간의 밀도 형성 확인
print(f"인지 공간 밀도: {result.get_latest_state().density:.4f}")
```

---

## 💡 고급 활용

### 예제 8: 동적 설정 업데이트

```python
engine = BoundaryConvergenceEngine()

# 초기 수렴
result1 = engine.converge()

# 설정 업데이트 후 재수렴
engine.update_config(
    error_threshold=1e-10,  # 더 정밀하게
    max_iterations=2000
)

result2 = engine.converge()
```

---

**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0

