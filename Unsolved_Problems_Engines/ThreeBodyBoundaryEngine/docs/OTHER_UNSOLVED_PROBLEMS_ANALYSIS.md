# 다른 난제 문제 적용 가능성 분석

**작성일**: 2026-02-03  
**엔진**: ThreeBodyBoundaryEngine (UP-1)  
**목적**: UP-1 구조가 다른 난제(나비효과, 스토크스 등)에 적용 가능한지 구조적 분석

---

## 🎯 핵심 질문

1. **UP-1 구조가 다른 난제에 적용 가능한가?**
2. **나비효과(Butterfly Effect)가 현재 구조에서 어떻게 표현되는가?**
3. **스토크스 방정식(Navier-Stokes)이 현재 구조에서 어떻게 표현되는가?**
4. **이 분석이 UP-1에 들어가는가, UP-2에 들어가는가, 별도 엔진인가?**

---

## 📐 UP-1 구조의 핵심 추상화

### 현재 구조 (삼체 문제)

```
입력: ThreeBodySystem (body1, body2, body3)
  ↓
중력 퍼텐셜 계산: V(x,y) = -G × Σ(m_i / r_i)
  ↓
밀도 변환: ρ(x,y) = V(x,y) / V_max
  ↓
경계 정합 분석: Δ = |P - 2πr| / 2πr + |A - πr²| / πr²
  ↓
안정성 판정: converged, mismatch, stability_score
  ↓
L1: 실패 기록 (Condition Signature)
  ↓
L2: 위험 지형 (SearchBias)
```

### 추상화 레벨

**핵심 추상화**:
1. **공간 변환**: 물리 법칙 → 밀도 필드
2. **경계 정합**: 밀도 → 경계 형성 시뮬레이션
3. **안정성 판정**: 경계 정합 실패 = 불안정
4. **실패 지형**: 조건 서명 → 위험도 맵

---

## 🦋 나비효과 (Butterfly Effect) 분석

### 나비효과의 본질

**정의**: 초기 조건의 미세한 차이가 시간에 따라 기하급수적으로 증폭되어 결과에 큰 차이를 만드는 현상

**수학적 표현**:
```
d(t) = d(0) × e^(λt)
```
- `d(0)`: 초기 조건 차이
- `λ`: Lyapunov 지수 (양수면 혼돈)
- `d(t)`: 시간 t에서의 차이

### UP-1 구조에서의 표현

#### 1. Condition Signature로 초기 조건 인코딩

**현재 구현** (`failure_atlas.py`):
```python
def _generate_condition_signature(
    self,
    system: ThreeBodySystem,
    analysis: StabilityAnalysis
) -> str:
    # 질량 비율
    masses = [b.mass for b in bodies]
    mass_ratio = tuple(sorted(masses, reverse=True))
    
    # 위치 패턴 (정규화된 거리)
    positions = [b.position for b in bodies]
    distances = []
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            dist = ((positions[i].x - positions[j].x) ** 2 + 
                   (positions[i].y - positions[j].y) ** 2) ** 0.5
            distances.append(round(dist, 2))
    
    signature = f"mass_{mass_ratio}_dist_{tuple(sorted(distances))}_mismatch_{analysis.mismatch:.3f}"
    return signature
```

**나비효과 관점**:
- **초기 조건 차이** = `condition_signature`의 미세한 차이
- **증폭** = `mismatch` 값의 급격한 증가
- **혼돈** = `convergence_rate < 0` (발산)

#### 2. FailureAtlas로 혼돈 패턴 축적

**현재 구현**:
```python
def get_similar_failures(
    self,
    condition_signature: str,
    similarity_threshold: float = 0.8
) -> List[FailureRecord]:
    """유사한 실패 패턴 찾기"""
```

**나비효과 관점**:
- **유사한 초기 조건** = `similarity_threshold`로 식별
- **다른 결과** = 같은 조건 서명인데 다른 `mismatch` 값
- **혼돈 지수** = `convergence_rate`의 분산

#### 3. 수식 매핑

**나비효과 수식**:
```
d(t) = d(0) × e^(λt)
```

**UP-1 구조 매핑**:
```
d(0) = |condition_signature_1 - condition_signature_2|
λ ≈ convergence_rate (음수면 발산 = 혼돈)
d(t) ≈ mismatch 차이
```

**구현 가능성**:
- ✅ **조건 서명 유사도** = 이미 구현됨
- ✅ **수렴 속도** = 이미 계산됨 (`convergence_rate`)
- ⚠️ **시간 적분** = UP-1은 정적 분석 (시간 없음)
- ⚠️ **Lyapunov 지수** = 직접 계산 안 함

---

## 🌊 스토크스 방정식 (Navier-Stokes) 분석

### 스토크스 방정식의 본질

**정의**: 점성 유체의 운동을 설명하는 비선형 편미분 방정식

**수식**:
```
∂u/∂t + (u·∇)u = -∇p/ρ + ν∇²u + f
∇·u = 0  (비압축성)
```

- `u`: 속도 벡터
- `p`: 압력
- `ρ`: 밀도
- `ν`: 점성 계수
- `f`: 외력

### UP-1 구조에서의 표현

#### 1. 밀도 필드로 유체 밀도 매핑

**현재 구현** (`gravity_calculator.py`):
```python
def potential_to_density(
    self,
    potential_field: Dict[Point, float],
    normalization: str = "max"
) -> Dict[Point, float]:
    """중력 퍼텐셜을 밀도로 변환"""
    # V(x,y) → ρ(x,y)
```

**스토크스 관점**:
- **중력 퍼텐셜** = 유체 밀도 분포의 원인
- **밀도 필드** = `ρ(x,y)` 직접 매핑 가능
- **경계** = 유체 경계 (자유 표면, 고체 경계)

#### 2. 경계 정합으로 유체 경계 형성

**현재 구현** (`boundary_convergence_adapter.py`):
```python
def converge(
    self,
    importance_weights: Dict[Point, float]
) -> ConvergenceResult:
    """경계 수렴 시뮬레이션"""
    # 밀도 가중치 → 경계 형성
```

**스토크스 관점**:
- **경계 형성** = 유체-공기 경계, 유체-고체 경계
- **정합 실패** = 난류(turbulence) 발생
- **불일치(Δ)** = 경계 불안정성

#### 3. 수식 매핑

**스토크스 방정식**:
```
∂u/∂t + (u·∇)u = -∇p/ρ + ν∇²u + f
```

**UP-1 구조 매핑**:
```
-∇p/ρ ≈ 중력 퍼텐셜 (V(x,y))
ρ ≈ 밀도 필드 (이미 계산됨)
경계 형성 ≈ 경계 정합 분석
난류 = 경계 정합 실패 (mismatch > threshold)
```

**구현 가능성**:
- ✅ **밀도 필드** = 이미 구현됨
- ✅ **경계 형성** = 이미 구현됨
- ❌ **속도 벡터 (u)** = UP-1은 정적 분석 (velocity 없음)
- ❌ **시간 적분** = UP-1은 시간 없음
- ❌ **압력 (p)** = 직접 계산 안 함

---

## 🔍 적용 가능성 결론

### ✅ 구조적으로 가능한 것

1. **나비효과 (초기 조건 민감성)**
   - ✅ Condition Signature로 초기 조건 인코딩
   - ✅ 유사 조건 찾기로 민감성 패턴 발견
   - ⚠️ 시간 적분 없어서 "증폭 과정" 직접 관찰 안 됨

2. **스토크스 (유체 경계 형성)**
   - ✅ 밀도 필드로 유체 밀도 매핑
   - ✅ 경계 정합으로 유체 경계 형성
   - ⚠️ 속도/압력 직접 계산 안 됨

### ❌ 구조적으로 불가능한 것

1. **시간 적분 필요**
   - 나비효과 증폭 과정
   - 스토크스 유체 운동

2. **벡터 필드 필요**
   - 스토크스 속도 벡터
   - 나비효과 궤적 추적

---

## 🎯 어디에 들어가는가? (UP-1 vs UP-2 vs 별도)

### UP-1에 들어가면 안 되는 이유

1. **정체성 보호**: UP-1은 "삼체 문제 원인 분석" 전용
2. **범위 고정**: 이미 봉인됨 (up-1.2.0)
3. **오해 방지**: "범용 엔진"으로 오해될 리스크

### UP-2에 들어가면 안 되는 이유

1. **역할 불일치**: UP-2는 "안전 탐색" (L3)
2. **입력 불일치**: UP-2는 `SearchBias` 입력, 나비효과/스토크스는 다른 입력 필요

### ✅ 결론: 별도 엔진 (UP-3, UP-4 등)

**UP-3: ButterflyEffectEngine (가칭)**
- 입력: 초기 조건 차이
- 출력: 민감성 지수, 혼돈 패턴
- 구조: UP-1의 Condition Signature + 시간 적분

**UP-4: NavierStokesBoundaryEngine (가칭)**
- 입력: 유체 밀도 분포
- 출력: 경계 형성 분석, 난류 발생 조건
- 구조: UP-1의 밀도 필드 + 경계 정합 + 속도 벡터

---

## 📋 구현 전략 (향후)

### Phase 1: 개념 문서화 ✅ (완료)

- [x] 나비효과/스토크스 구조적 분석
- [x] UP-1 구조와의 매핑
- [x] 적용 가능성/불가능성 명확화

### Phase 2: 별도 엔진 설계 (향후)

- [ ] UP-3 설계 문서 (나비효과)
- [ ] UP-4 설계 문서 (스토크스)
- [ ] 공통 인터페이스 정의

### Phase 3: 구현 (장기)

- [ ] UP-3 구현
- [ ] UP-4 구현
- [ ] 통합 테스트

---

## 🔬 핵심 인사이트

### 1. UP-1의 추상화 레벨

**UP-1은 "경계 정합 관점"의 추상화**:
- 물리 법칙 → 밀도 필드
- 밀도 필드 → 경계 형성
- 경계 형성 → 안정성 판정

**이 추상화는 다른 난제에도 적용 가능**:
- 나비효과: 초기 조건 → 민감성 패턴
- 스토크스: 유체 밀도 → 경계 형성

### 2. 제약 조건

**UP-1의 제약**:
- 정적 분석 (시간 없음)
- 스칼라 필드만 (벡터 없음)

**이 제약 때문에**:
- 나비효과 "증폭 과정" 직접 관찰 불가
- 스토크스 "유체 운동" 직접 계산 불가

**하지만**:
- "원인 조건" 분석은 가능
- "경계 형성 실패" 분석은 가능

### 3. 범용화 전략

**UP-1을 범용화하려면**:
- 시간 적분 추가 → 별도 엔진
- 벡터 필드 추가 → 별도 엔진
- 도메인 특화 로직 분리 → 별도 엔진

**결론**: UP-1은 그대로 두고, **별도 엔진으로 확장**

---

## ✅ 최종 판정

1. **나비효과/스토크스 적용 가능성**: ✅ 구조적으로 가능 (제약 있음)
2. **UP-1에 들어가는가**: ❌ 안 됨 (정체성/범위 보호)
3. **UP-2에 들어가는가**: ❌ 안 됨 (역할 불일치)
4. **별도 엔진인가**: ✅ 맞음 (UP-3, UP-4 등)

**다음 단계**: UP-3, UP-4 설계 문서 작성 (구현은 향후)

---

**작성자**: GNJz (Qquarts)  
**작성일**: 2026-02-03  
**상태**: 분석 완료 ✅

