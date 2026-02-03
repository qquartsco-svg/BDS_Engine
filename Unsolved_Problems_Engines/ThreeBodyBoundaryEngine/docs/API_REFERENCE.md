# API Reference - ThreeBodyBoundaryEngine

**엔진 번호**: UP-1  
**버전**: 1.2.0  
**최종 업데이트**: 2026-02-03

---

## 📚 목차

1. [L0: 원인 분석 레이어](#l0-원인-분석-레이어)
2. [L1: 실패 추적 레이어](#l1-실패-추적-레이어)
3. [L2: 실패 학습 레이어](#l2-실패-학습-레이어)
4. [데이터 모델](#데이터-모델)
5. [에러 처리](#에러-처리)

---

## L0: 원인 분석 레이어

### `ThreeBodyBoundaryEngine`

삼체 문제를 경계 정합 관점에서 분석하는 엔진.

#### 생성자

```python
ThreeBodyBoundaryEngine(config: Optional[ThreeBodyConfig] = None)
```

**매개변수**:
- `config` (Optional[ThreeBodyConfig]): 설정 객체. None이면 기본값 사용.

**반환값**: `ThreeBodyBoundaryEngine` 인스턴스

**예제**:
```python
from three_body_boundary_engine import ThreeBodyBoundaryEngine, ThreeBodyConfig

# 기본 설정으로 생성
engine = ThreeBodyBoundaryEngine()

# 커스텀 설정으로 생성
config = ThreeBodyConfig(
    boundary_radius=2.0,
    max_iterations=1000
)
engine = ThreeBodyBoundaryEngine(config)
```

---

#### `analyze_orbit_stability()`

궤도 안정성 분석

```python
analyze_orbit_stability(
    system: ThreeBodySystem,
    x_range: Optional[tuple] = None,
    y_range: Optional[tuple] = None
) -> StabilityAnalysis
```

**매개변수**:
- `system` (ThreeBodySystem): 분석할 삼체 시스템
- `x_range` (Optional[tuple]): x 범위 (min, max). None이면 자동 계산.
- `y_range` (Optional[tuple]): y 범위 (min, max). None이면 자동 계산.

**반환값**: `StabilityAnalysis` - 안정성 분석 결과

**예제**:
```python
from three_body_boundary_engine import ThreeBodySystem, Body, Point

system = ThreeBodySystem(
    body1=Body(position=Point(0.0, 0.0), mass=1.0),
    body2=Body(position=Point(1.0, 0.0), mass=1.0),
    body3=Body(position=Point(0.5, 0.866), mass=1.0)
)

analysis = engine.analyze_orbit_stability(system)
print(f"안정 여부: {analysis.is_stable()}")
print(f"안정성 점수: {analysis.stability_score:.3f}")
```

---

#### `observe_boundary_formation()`

경계 형성 과정 관찰

```python
observe_boundary_formation(
    system: ThreeBodySystem,
    time_steps: List[float],
    x_range: Optional[tuple] = None,
    y_range: Optional[tuple] = None
) -> BoundaryDynamics
```

**매개변수**:
- `system` (ThreeBodySystem): 분석할 삼체 시스템
- `time_steps` (List[float]): 관찰할 시간 단계 리스트
- `x_range` (Optional[tuple]): x 범위. None이면 자동 계산.
- `y_range` (Optional[tuple]): y 범위. None이면 자동 계산.

**반환값**: `BoundaryDynamics` - 경계 동역학 관찰 결과

**예제**:
```python
time_steps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
dynamics = engine.observe_boundary_formation(system, time_steps)

collapse_point = dynamics.get_collapse_point(threshold=1.0)
if collapse_point:
    print(f"붕괴 시점: {collapse_point}")
```

---

#### `observe_lagrange_points()`

라그랑주 점 경계 관찰

```python
observe_lagrange_points(
    system: ThreeBodySystem
) -> LagrangeAnalysis
```

**매개변수**:
- `system` (ThreeBodySystem): 분석할 삼체 시스템

**반환값**: `LagrangeAnalysis` - 라그랑주 점 분석 결과

**예제**:
```python
lagrange_analysis = engine.observe_lagrange_points(system)

for lp in lagrange_analysis.lagrange_points:
    print(f"{lp.lagrange_type}: {lp.stability}")
```

---

#### `compare_stability_conditions()`

안정/불안정 조건 비교

```python
compare_stability_conditions(
    systems: List[ThreeBodySystem],
    x_range: Optional[tuple] = None,
    y_range: Optional[tuple] = None
) -> List[StabilityAnalysis]
```

**매개변수**:
- `systems` (List[ThreeBodySystem]): 비교할 삼체 시스템 리스트
- `x_range` (Optional[tuple]): x 범위. None이면 자동 계산.
- `y_range` (Optional[tuple]): y 범위. None이면 자동 계산.

**반환값**: `List[StabilityAnalysis]` - 각 시스템의 안정성 분석 결과 리스트

**예제**:
```python
systems = [system1, system2, system3]
results = engine.compare_stability_conditions(systems)

for i, result in enumerate(results):
    print(f"시스템 {i+1}: 안정 여부 = {result.is_stable()}")
```

---

## L1: 실패 추적 레이어

### `FailureAtlas`

실패 패턴을 구조화하여 저장하고 분류하는 레이어.

#### 생성자

```python
FailureAtlas()
```

**반환값**: `FailureAtlas` 인스턴스

**예제**:
```python
from three_body_boundary_engine import FailureAtlas

atlas = FailureAtlas()
```

---

#### `record_failure()`

실패 기록 추가

```python
record_failure(
    analysis: StabilityAnalysis,
    system: ThreeBodySystem,
    threshold: float = 0.1
) -> Optional[FailureRecord]
```

**매개변수**:
- `analysis` (StabilityAnalysis): L0의 안정성 분석 결과
- `system` (ThreeBodySystem): 삼체 시스템
- `threshold` (float): 실패 임계값. 기본값 0.1.

**반환값**: `Optional[FailureRecord]` - 실패 기록. 안정적이면 None.

**예제**:
```python
analysis = engine.analyze_orbit_stability(system)
record = atlas.record_failure(analysis, system, threshold=0.1)

if record:
    print(f"실패 기록됨: {record.collapse_mode.value}")
    print(f"심각도: {record.collapse_severity:.3f}")
```

---

#### `get_similar_failures()`

유사한 실패 패턴 찾기

```python
get_similar_failures(
    condition_signature: str,
    similarity_threshold: float = 0.8
) -> List[FailureRecord]
```

**매개변수**:
- `condition_signature` (str): 비교할 조건 서명
- `similarity_threshold` (float): 유사도 임계값 (0.0 ~ 1.0). 기본값 0.8.

**반환값**: `List[FailureRecord]` - 유사한 실패 기록 리스트

**예제**:
```python
if len(atlas.failure_records) > 0:
    first_record = atlas.failure_records[0]
    similar = atlas.get_similar_failures(
        condition_signature=first_record.condition_signature,
        similarity_threshold=0.5
    )
    print(f"유사한 실패 패턴: {len(similar)}개")
```

---

#### `get_failure_statistics()`

실패 통계 반환

```python
get_failure_statistics() -> Dict
```

**반환값**: `Dict` - 실패 통계 딕셔너리

**통계 내용**:
- `total_failures`: 총 실패 횟수
- `failure_by_mode`: 붕괴 모드별 실패 횟수
- `failure_rate_by_mode`: 붕괴 모드별 실패율
- `failure_by_type`: 실패 유형별 실패 횟수

**예제**:
```python
stats = atlas.get_failure_statistics()
print(f"총 실패 횟수: {stats['total_failures']}")
print(f"붕괴 모드별 분류: {stats['failure_by_mode']}")
```

---

#### `clear()`

모든 기록 초기화

```python
clear() -> None
```

**예제**:
```python
atlas.clear()
print(f"기록 수: {len(atlas.failure_records)}")  # 0
```

---

## L2: 실패 학습 레이어

> **⚠️ 중요 명확화**: 본 레이어는 어떠한 정책, 행동, 해결책도 생성하지 않습니다.  
> 오직 탐색 공간에서의 위험 지형만을 형성합니다.  
> 최적화나 강화학습이 아닙니다.

### `FailureBiasConverter`

실패 패턴을 탐색 편향으로 변환하는 레이어.

**핵심 원칙**:
- ❌ 정책 생성 안 함
- ❌ 행동 지시 안 함
- ❌ 해결책 제시 안 함
- ✅ 위험 지형만 형성

#### 생성자

```python
FailureBiasConverter(
    risk_decay_factor: float = 0.9,
    min_risk_threshold: float = 0.1
)
```

**매개변수**:
- `risk_decay_factor` (float): 위험도 감쇠 계수 (0.0 ~ 1.0). 기본값 0.9.
- `min_risk_threshold` (float): 최소 위험도 임계값. 기본값 0.1.

**예제**:
```python
from three_body_boundary_engine import FailureBiasConverter

converter = FailureBiasConverter(
    risk_decay_factor=0.9,
    min_risk_threshold=0.1
)
```

---

#### `convert_failure_to_bias()`

실패 패턴을 탐색 편향으로 변환

```python
convert_failure_to_bias(
    failure_atlas: FailureAtlas
) -> SearchBias
```

**매개변수**:
- `failure_atlas` (FailureAtlas): L1의 실패 지도

**반환값**: `SearchBias` - 탐색 편향

**예제**:
```python
bias = converter.convert_failure_to_bias(atlas)
print(f"총 위험도 점수: {bias.total_risk_score:.3f}")
print(f"최대 위험도 점수: {bias.max_risk_score:.3f}")
```

---

#### `should_avoid_condition()`

조건을 회피해야 하는지 판정

```python
should_avoid_condition(
    bias: SearchBias,
    condition_signature: str,
    threshold: float = 0.5
) -> bool
```

**매개변수**:
- `bias` (SearchBias): 탐색 편향
- `condition_signature` (str): 조건 서명
- `threshold` (float): 회피 임계값. 기본값 0.5.

**반환값**: `bool` - 회피 여부

**예제**:
```python
should_avoid = converter.should_avoid_condition(
    bias=bias,
    condition_signature=condition_sig,
    threshold=0.3
)

if should_avoid:
    print("이 조건은 회피해야 합니다")
```

---

#### `get_safe_conditions()`

안전한 조건 필터링

```python
get_safe_conditions(
    bias: SearchBias,
    candidate_conditions: List[str],
    threshold: float = 0.5
) -> List[str]
```

**매개변수**:
- `bias` (SearchBias): 탐색 편향
- `candidate_conditions` (List[str]): 후보 조건 서명 리스트
- `threshold` (float): 안전 임계값. 기본값 0.5.

**반환값**: `List[str]` - 안전한 조건 리스트

**예제**:
```python
candidates = ["condition1", "condition2", "condition3"]
safe = converter.get_safe_conditions(
    bias=bias,
    candidate_conditions=candidates,
    threshold=0.3
)
print(f"안전한 조건: {len(safe)}개")
```

---

#### `update_bias_with_new_failure()`

새로운 실패 기록으로 편향 업데이트

```python
update_bias_with_new_failure(
    bias: SearchBias,
    new_record: FailureRecord
) -> SearchBias
```

**매개변수**:
- `bias` (SearchBias): 기존 탐색 편향
- `new_record` (FailureRecord): 새로운 실패 기록

**반환값**: `SearchBias` - 업데이트된 탐색 편향

**예제**:
```python
new_record = atlas.record_failure(analysis, system)
if new_record:
    updated_bias = converter.update_bias_with_new_failure(
        bias=bias,
        new_record=new_record
    )
```

---

## 데이터 모델

### `StabilityAnalysis`

안정성 분석 결과

**속성**:
- `converged` (bool): 수렴 여부
- `mismatch` (float): 경계 불일치
- `iteration` (int): 반복 횟수
- `boundary_points` (int): 경계 점 개수
- `stability_score` (float): 안정성 점수 (0.0 ~ 1.0)
- `convergence_rate` (float): 수렴 속도

**메서드**:
- `is_stable(threshold: float = 0.1) -> bool`: 안정 여부 판정

---

### `FailureRecord`

실패 기록

**속성**:
- `condition_signature` (str): 조건 서명
- `timestamp` (float): 발생 시점
- `delta_threshold_crossed` (float): Δ 임계값 초과
- `mismatch` (float): 경계 불일치
- `convergence_rate` (float): 수렴 속도
- `converged` (bool): 수렴 여부
- `stability_score` (float): 안정성 점수
- `collapse_mode` (CollapseMode): 붕괴 모드
- `collapse_severity` (float): 붕괴 심각도 (0.0 ~ 1.0)
- `spatial_pattern` (Optional[Dict[str, float]]): 공간 패턴
- `iteration` (int): 반복 횟수
- `boundary_points` (int): 경계 점 개수

**메서드**:
- `get_failure_type() -> str`: 실패 유형 반환

---

### `SearchBias`

탐색 편향

**속성**:
- `risk_map` (Dict[str, float]): 위험 지도 (조건 서명별 위험도)
- `collapse_mode_risk` (Dict[str, float]): 붕괴 모드별 위험도
- `spatial_risk_pattern` (Optional[Dict[Tuple[float, float], float]]): 공간 패턴별 위험도
- `total_risk_score` (float): 전체 위험도 점수
- `max_risk_score` (float): 최대 위험도 점수

**메서드**:
- `get_risk(condition_signature: str) -> float`: 조건 서명에 대한 위험도 반환
- `is_risky(condition_signature: str, threshold: float = 0.5) -> bool`: 위험한 조건인지 판정

---

### `CollapseMode`

붕괴 모드 열거형

**값**:
- `DIVERGENCE`: 발산 (convergence_rate < 0)
- `MISMATCH`: 불일치 (mismatch > threshold)
- `CONVERGENCE_FAILURE`: 수렴 실패 (converged = False)
- `UNKNOWN`: 알 수 없음

---

## 에러 처리

### 일반적인 에러

#### `ValueError`

**발생 조건**:
- 질량이 0 이하인 경우
- 잘못된 범위 값

**예제**:
```python
try:
    body = Body(position=Point(0, 0), mass=-1.0)  # ValueError 발생
except ValueError as e:
    print(f"에러: {e}")
```

#### `TypeError`

**발생 조건**:
- 잘못된 타입의 매개변수 전달

**예제**:
```python
try:
    analysis = engine.analyze_orbit_stability("invalid")  # TypeError 발생
except TypeError as e:
    print(f"에러: {e}")
```

---

### 레이어별 에러 처리

#### L0 (ThreeBodyBoundaryEngine)

- 입력 검증: `ThreeBodySystem`의 유효성 검사
- 범위 계산: 자동 계산 실패 시 기본값 사용

#### L1 (FailureAtlas)

- 실패 기록: 안정적인 경우 `None` 반환 (에러 아님)
- 유사도 계산: 빈 기록 리스트인 경우 빈 리스트 반환

#### L2 (FailureBiasConverter)

- 빈 Atlas: 실패 기록이 없으면 빈 `SearchBias` 반환
- 위험도 계산: 최소 임계값 미만은 자동 필터링

---

## 버전 정보

- **1.2.0** (2026-02-03): L1, L2 레이어 추가
- **1.1.0** (2026-02-02): 원인 분석 전용으로 명확화
- **1.0.0** (2026-02-02): 초기 릴리스

---

**작성자**: GNJz (Qquarts)  
**최종 업데이트**: 2026-02-03

