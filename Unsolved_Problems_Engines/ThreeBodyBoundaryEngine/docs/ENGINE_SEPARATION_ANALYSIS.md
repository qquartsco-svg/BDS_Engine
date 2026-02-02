# 원인 분석 엔진 vs 해결 탐색 엔진 분리 분석

**작성일**: 2026-02-02  
**분석 목적**: 엔진 모듈화 필요성 평가

---

## 📊 현재 구조

### 현재 상태: 통합 엔진

**ThreeBodyBoundaryEngine**에 포함된 기능:

1. **원인 분석 기능** (Causal Analysis)
   - `analyze_orbit_stability()` ✅ 완성, 작동
   - `observe_boundary_formation()` ✅ 완성, 작동
   - `observe_lagrange_points()` ✅ 완성, 작동
   - `compare_stability_conditions()` ✅ 완성, 작동

2. **해결 탐색 기능** (Solution Approach)
   - `recover_boundary_alignment()` ❌ 프로토타입, 작동 안 함
   - `stabilize_system()` ❌ 프로토타입, 작동 안 함
   - `apply_dynamic_correction()` ❌ 프로토타입, 작동 안 함

---

## 🔍 분리 필요성 분석

### 옵션 1: 통합 유지 (현재 상태)

**장점**:
- ✅ 단일 엔진으로 사용 편리
- ✅ 공통 데이터 구조 공유
- ✅ 코드 중복 없음
- ✅ 통합 테스트 용이

**단점**:
- ❌ 원인 분석과 해결 탐색의 완성도 차이
- ❌ 해결 탐색이 미완성 상태로 공개됨
- ❌ 독립 배포 불가능
- ❌ 의존성 혼재

**적용 시나리오**:
- 연구/개발 단계
- 내부 사용
- 프로토타입 단계

---

### 옵션 2: 완전 분리 (독립 엔진)

**구조**:
```
ThreeBodyBoundaryEngine (원인 분석)
├── analyze_orbit_stability()
├── observe_boundary_formation()
├── observe_lagrange_points()
└── compare_stability_conditions()

ThreeBodySolutionEngine (해결 탐색)
├── recover_boundary_alignment()
├── stabilize_system()
└── apply_dynamic_correction()
```

**장점**:
- ✅ 독립 배포 가능
- ✅ 완성도별 배포 가능
- ✅ 의존성 분리
- ✅ 버전 관리 독립
- ✅ 사용자가 필요한 것만 선택 가능

**단점**:
- ❌ 코드 중복 가능성
- ❌ 공통 데이터 구조 분리 필요
- ❌ 통합 사용 시 두 엔진 필요
- ❌ 유지보수 복잡도 증가

**적용 시나리오**:
- 프로덕션 배포
- 상업적 사용
- 완성도가 다른 기능 분리

---

### 옵션 3: 하이브리드 (통합 + 선택적 분리)

**구조**:
```
ThreeBodyBoundaryEngine (통합)
├── 원인 분석 기능 (항상 포함)
└── 해결 탐색 기능 (선택적 포함)

ThreeBodySolutionEngine (독립, 선택적)
└── 해결 탐색 기능만 (ThreeBodyBoundaryEngine 의존)
```

**장점**:
- ✅ 기본은 통합, 필요시 분리
- ✅ 원인 분석은 독립 사용 가능
- ✅ 해결 탐색은 선택적 사용
- ✅ 유연한 배포 전략

**단점**:
- ❌ 구조 복잡도 증가
- ❌ 의존성 관리 필요
- ❌ 문서화 복잡

**적용 시나리오**:
- 단계적 배포
- 유연한 사용 모델
- 완성도별 배포

---

## 📋 비교표

| 항목 | 통합 유지 | 완전 분리 | 하이브리드 |
|------|----------|----------|-----------|
| 사용 편의성 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 독립 배포 | ❌ | ✅ | ⚠️ |
| 완성도 분리 | ❌ | ✅ | ⚠️ |
| 코드 중복 | 없음 | 가능 | 가능 |
| 유지보수 | 쉬움 | 복잡 | 중간 |
| 배포 전략 | 단일 | 독립 | 유연 |
| 의존성 | 혼재 | 분리 | 선택적 |

---

## 🎯 권장 사항

### 단기 (현재 ~ 1개월)

**권장**: 통합 유지 + 해결 탐색 기능 비활성화

**이유**:
- 원인 분석 기능은 완성되어 사용 가능
- 해결 탐색 기능은 프로토타입 단계
- 단일 엔진으로 관리 용이

**구현 방법**:
```python
class ThreeBodyBoundaryEngine:
    def __init__(self, enable_solution: bool = False):
        self.enable_solution = enable_solution
    
    def recover_boundary_alignment(self, ...):
        if not self.enable_solution:
            raise NotImplementedError("Solution approach is in prototype stage")
        # ... 구현
```

---

### 중기 (1-3개월)

**권장**: 하이브리드 구조

**이유**:
- 원인 분석은 독립 배포 가능
- 해결 탐색은 선택적 사용
- 단계적 완성도 향상

**구조**:
```
ThreeBodyBoundaryEngine (v1.0.0) - 원인 분석만
ThreeBodySolutionEngine (v0.1.0) - 해결 탐색 (의존: BoundaryEngine)
ThreeBodyEngine (v1.0.0) - 통합 (선택적)
```

---

### 장기 (3개월 이후)

**권장**: 완전 분리 (조건부)

**조건**:
- 해결 탐색 기능이 완성되었을 때
- 독립 배포가 필요할 때
- 상업적 사용이 시작될 때

**구조**:
```
ThreeBodyBoundaryEngine (v2.0.0) - 원인 분석만
ThreeBodySolutionEngine (v1.0.0) - 해결 탐색만
```

---

## 🔧 구현 방안

### 방안 1: 기능 플래그 (즉시 적용 가능)

```python
class ThreeBodyBoundaryEngine:
    def __init__(self, config=None, enable_solution=False):
        self.config = config or ThreeBodyConfig()
        self.enable_solution = enable_solution
        # ... 초기화
    
    def recover_boundary_alignment(self, ...):
        if not self.enable_solution:
            raise NotImplementedError(
                "Solution approach is in prototype stage. "
                "Set enable_solution=True to use (not recommended for production)"
            )
        # ... 구현
```

**장점**: 즉시 적용 가능, 기존 코드 유지

---

### 방안 2: 별도 클래스 (중기)

```python
# 원인 분석 전용
class ThreeBodyBoundaryEngine:
    # 원인 분석 메서드만

# 해결 탐색 전용
class ThreeBodySolutionEngine:
    def __init__(self, boundary_engine: ThreeBodyBoundaryEngine):
        self.boundary_engine = boundary_engine
    # 해결 탐색 메서드만

# 통합 (선택적)
class ThreeBodyEngine:
    def __init__(self):
        self.boundary = ThreeBodyBoundaryEngine()
        self.solution = ThreeBodySolutionEngine(self.boundary)
```

**장점**: 명확한 분리, 독립 배포 가능

---

### 방안 3: 완전 분리 (장기)

```
three-body-boundary-engine/ (PyPI 패키지)
└── 원인 분석만

three-body-solution-engine/ (PyPI 패키지)
└── 해결 탐색만 (의존: three-body-boundary-engine)
```

**장점**: 완전 독립, 버전 관리 독립

---

## 📊 의사결정 매트릭스

### 분리가 필요한 경우

✅ **YES, 분리 필요**:
- 해결 탐색 기능이 완성되었을 때
- 독립 배포가 필요할 때
- 상업적 사용이 시작될 때
- 완성도가 크게 다를 때

❌ **NO, 통합 유지**:
- 연구/개발 단계
- 내부 사용만
- 프로토타입 단계
- 완성도가 비슷할 때

---

## 🎯 최종 권장사항

### 현재 단계 (즉시)

**권장**: 기능 플래그 방식

1. `enable_solution=False` (기본값)
2. 해결 탐색 기능은 비활성화 상태로 유지
3. 원인 분석 기능만 활성화

**이유**:
- 기존 코드 유지
- 사용자 혼란 방지
- 단계적 완성도 향상

### 다음 단계 (1-3개월)

**권장**: 하이브리드 구조

1. 원인 분석 엔진 독립 배포
2. 해결 탐색 엔진 선택적 배포
3. 통합 엔진 제공 (선택적)

### 최종 단계 (3개월 이후)

**권장**: 완전 분리 (조건부)

1. 해결 탐색 기능 완성 시
2. 독립 배포 필요 시
3. 상업적 사용 시작 시

---

## 📝 체크리스트

### 분리 전 확인사항

- [ ] 해결 탐색 기능의 완성도
- [ ] 독립 배포 필요성
- [ ] 사용자 요구사항
- [ ] 유지보수 계획
- [ ] 버전 관리 전략

### 분리 시 작업

- [ ] 코드 분리
- [ ] 의존성 정리
- [ ] 테스트 분리
- [ ] 문서화 분리
- [ ] 배포 전략 수립

---

**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0

