# 사용 가이드 - ThreeBodyBoundaryEngine

**엔진 번호**: UP-1  
**버전**: 1.2.0  
**최종 업데이트**: 2026-02-03

---

## 📚 목차

1. [빠른 시작](#빠른-시작)
2. [레이어별 사용법](#레이어별-사용법)
3. [통합 사용 예제](#통합-사용-예제)
4. [베스트 프랙티스](#베스트-프랙티스)
5. [자주 묻는 질문](#자주-묻는-질문)

---

## 빠른 시작

### 기본 사용법

```python
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodySystem,
    Body,
    Point
)

# 엔진 생성
engine = ThreeBodyBoundaryEngine()

# 삼체 시스템 생성
system = ThreeBodySystem(
    body1=Body(position=Point(0.0, 0.0), mass=1.0),
    body2=Body(position=Point(1.0, 0.0), mass=1.0),
    body3=Body(position=Point(0.5, 0.866), mass=1.0)
)

# 안정성 분석
analysis = engine.analyze_orbit_stability(system)

# 결과 확인
print(f"안정 여부: {analysis.is_stable()}")
print(f"안정성 점수: {analysis.stability_score:.3f}")
```

---

## 레이어별 사용법

### L0: 원인 분석 레이어

#### 기본 분석

```python
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodySystem,
    Body,
    Point
)

engine = ThreeBodyBoundaryEngine()

system = ThreeBodySystem(
    body1=Body(position=Point(0.0, 0.0), mass=1.0),
    body2=Body(position=Point(1.0, 0.0), mass=1.0),
    body3=Body(position=Point(0.5, 0.866), mass=1.0)
)

# 안정성 분석
analysis = engine.analyze_orbit_stability(system)

if analysis.is_stable():
    print("안정적인 시스템")
else:
    print(f"불안정: mismatch = {analysis.mismatch:.6f}")
```

#### 경계 형성 과정 관찰

```python
# 시간 단계 정의
time_steps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]

# 경계 형성 관찰
dynamics = engine.observe_boundary_formation(system, time_steps)

# 붕괴 시점 확인
collapse_point = dynamics.get_collapse_point(threshold=1.0)
if collapse_point:
    print(f"붕괴 시점: {collapse_point}")
```

#### 라그랑주 점 분석

```python
# 라그랑주 점 관찰
lagrange_analysis = engine.observe_lagrange_points(system)

for lp in lagrange_analysis.lagrange_points:
    print(f"{lp.lagrange_type}: {lp.stability}")
```

---

### L1: 실패 추적 레이어

#### 실패 기록

```python
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    FailureAtlas,
    ThreeBodySystem,
    Body,
    Point
)

# L0 엔진
engine = ThreeBodyBoundaryEngine()

# L1 Atlas
atlas = FailureAtlas()

# 시스템 분석
system = ThreeBodySystem(
    body1=Body(position=Point(0.0, 0.0), mass=1.0),
    body2=Body(position=Point(1.0, 0.0), mass=1.0),
    body3=Body(position=Point(0.5, 0.866), mass=1.0)
)

analysis = engine.analyze_orbit_stability(system)

# 실패 기록
record = atlas.record_failure(
    analysis=analysis,
    system=system,
    threshold=0.1
)

if record:
    print(f"실패 기록됨:")
    print(f"  - 붕괴 모드: {record.collapse_mode.value}")
    print(f"  - 심각도: {record.collapse_severity:.3f}")
    print(f"  - 조건 서명: {record.condition_signature[:50]}...")
```

#### 실패 통계 확인

```python
# 여러 시스템 분석 및 기록
systems = [system1, system2, system3]

for system in systems:
    analysis = engine.analyze_orbit_stability(system)
    atlas.record_failure(analysis, system, threshold=0.1)

# 통계 확인
stats = atlas.get_failure_statistics()
print(f"총 실패 횟수: {stats['total_failures']}")
print(f"붕괴 모드별 분류: {stats['failure_by_mode']}")
```

#### 유사한 실패 패턴 찾기

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

### L2: 실패 학습 레이어

#### 편향 생성

```python
from three_body_boundary_engine import (
    FailureAtlas,
    FailureBiasConverter
)

# L1 Atlas (이미 실패 기록이 있다고 가정)
atlas = FailureAtlas()
# ... 실패 기록 추가 ...

# L2 Converter
converter = FailureBiasConverter(
    risk_decay_factor=0.9,
    min_risk_threshold=0.1
)

# 편향 생성
bias = converter.convert_failure_to_bias(atlas)

print(f"총 위험도 점수: {bias.total_risk_score:.3f}")
print(f"최대 위험도 점수: {bias.max_risk_score:.3f}")
```

#### 조건 회피 판정

```python
# 조건 서명
condition_sig = "mass_(1.0, 1.0, 1.0)_dist_(1.0, 1.0, 1.0)_mismatch_0.000"

# 회피 판정
should_avoid = converter.should_avoid_condition(
    bias=bias,
    condition_signature=condition_sig,
    threshold=0.3
)

if should_avoid:
    print("이 조건은 회피해야 합니다")
else:
    print("이 조건은 안전합니다")
```

#### 안전한 조건 필터링

```python
# 후보 조건 리스트
candidate_conditions = [
    "condition1",
    "condition2",
    "condition3"
]

# 안전한 조건 필터링
safe_conditions = converter.get_safe_conditions(
    bias=bias,
    candidate_conditions=candidate_conditions,
    threshold=0.3
)

print(f"안전한 조건: {len(safe_conditions)}개")
```

#### 편향 업데이트

```python
# 새로운 실패 기록
new_record = atlas.record_failure(analysis, system)

if new_record:
    # 편향 업데이트
    updated_bias = converter.update_bias_with_new_failure(
        bias=bias,
        new_record=new_record
    )
    
    print(f"업데이트 전: {bias.total_risk_score:.3f}")
    print(f"업데이트 후: {updated_bias.total_risk_score:.3f}")
```

---

## 통합 사용 예제

### L0 + L1 통합

```python
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    FailureAtlas,
    ThreeBodySystem,
    Body,
    Point
)

# 엔진 생성
engine = ThreeBodyBoundaryEngine()
atlas = FailureAtlas()

# 여러 시스템 분석
systems = [
    ThreeBodySystem(
        body1=Body(position=Point(0.0, 0.0), mass=1.0),
        body2=Body(position=Point(1.0, 0.0), mass=1.0),
        body3=Body(position=Point(0.5, 0.866), mass=1.0)
    ),
    # ... 더 많은 시스템 ...
]

# 분석 및 기록
for system in systems:
    analysis = engine.analyze_orbit_stability(system)
    record = atlas.record_failure(analysis, system, threshold=0.1)
    
    if record:
        print(f"실패 기록: {record.collapse_mode.value}")

# 통계 확인
stats = atlas.get_failure_statistics()
print(f"총 실패 횟수: {stats['total_failures']}")
```

---

### L0 + L1 + L2 통합

```python
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    FailureAtlas,
    FailureBiasConverter,
    ThreeBodySystem,
    Body,
    Point
)

# 엔진 생성
engine = ThreeBodyBoundaryEngine()
atlas = FailureAtlas()
converter = FailureBiasConverter()

# 시스템 분석 및 기록
system = ThreeBodySystem(
    body1=Body(position=Point(0.0, 0.0), mass=1.0),
    body2=Body(position=Point(1.0, 0.0), mass=1.0),
    body3=Body(position=Point(0.5, 0.866), mass=1.0)
)

analysis = engine.analyze_orbit_stability(system)
atlas.record_failure(analysis, system, threshold=0.1)

# 편향 생성
bias = converter.convert_failure_to_bias(atlas)

# 위험한 조건 회피
condition_sig = atlas.failure_records[0].condition_signature
should_avoid = converter.should_avoid_condition(
    bias=bias,
    condition_signature=condition_sig,
    threshold=0.3
)

print(f"회피 여부: {should_avoid}")
```

---

## 베스트 프랙티스

### 1. 레이어별 독립 사용

각 레이어는 독립적으로 사용 가능하지만, 통합 사용을 권장합니다.

```python
# ✅ 권장: 통합 사용
engine = ThreeBodyBoundaryEngine()
atlas = FailureAtlas()
converter = FailureBiasConverter()

# L0 → L1 → L2 파이프라인
analysis = engine.analyze_orbit_stability(system)
atlas.record_failure(analysis, system)
bias = converter.convert_failure_to_bias(atlas)
```

---

### 2. 임계값 조정

임계값은 사용 사례에 따라 조정하세요.

```python
# 실패 기록 임계값
record = atlas.record_failure(
    analysis=analysis,
    system=system,
    threshold=0.1  # 조정 가능
)

# 회피 판정 임계값
should_avoid = converter.should_avoid_condition(
    bias=bias,
    condition_signature=condition_sig,
    threshold=0.3  # 조정 가능
)
```

---

### 3. 실패 기록 관리

대량의 실패 기록이 쌓이면 주기적으로 정리하세요.

```python
# 주기적으로 Atlas 초기화
if atlas.total_failures > 10000:
    atlas.clear()
    print("Atlas 초기화됨")
```

---

### 4. 편향 업데이트 전략

새로운 실패가 발생할 때마다 편향을 업데이트하세요.

```python
# 실패 발생 시 즉시 업데이트
new_record = atlas.record_failure(analysis, system)
if new_record:
    bias = converter.update_bias_with_new_failure(
        bias=bias,
        new_record=new_record
    )
```

---

### 5. 에러 처리

에러 처리를 명시적으로 구현하세요.

```python
try:
    analysis = engine.analyze_orbit_stability(system)
except ValueError as e:
    print(f"에러: {e}")
    # 에러 처리 로직
```

---

## 자주 묻는 질문

### Q1: L0만 사용해도 되나요?

**A**: 네, 가능합니다. L0는 독립적으로 사용 가능합니다.

```python
engine = ThreeBodyBoundaryEngine()
analysis = engine.analyze_orbit_stability(system)
```

하지만 실패 패턴을 추적하려면 L1, L2를 함께 사용하는 것을 권장합니다.

---

### Q2: L1과 L2는 반드시 함께 사용해야 하나요?

**A**: 아니요. L1은 독립적으로 사용 가능합니다.

```python
# L1만 사용
atlas = FailureAtlas()
atlas.record_failure(analysis, system)
stats = atlas.get_failure_statistics()
```

L2는 L1의 출력을 입력으로 받으므로, L1 없이는 사용할 수 없습니다.

---

### Q3: 실패 기록이 너무 많아지면 어떻게 하나요?

**A**: 주기적으로 Atlas를 초기화하거나, 오래된 기록을 필터링하세요.

```python
# 방법 1: 초기화
atlas.clear()

# 방법 2: 최근 N개만 유지
if len(atlas.failure_records) > 1000:
    atlas.failure_records = atlas.failure_records[-1000:]
```

---

### Q4: 편향의 위험도는 어떻게 해석하나요?

**A**: 위험도는 0.0 ~ 1.0 사이의 값입니다.

- **0.0 ~ 0.3**: 안전한 조건
- **0.3 ~ 0.7**: 주의 필요한 조건
- **0.7 ~ 1.0**: 위험한 조건 (회피 권장)

---

### Q5: L3는 언제 사용할 수 있나요?

**A**: L3는 아직 구현되지 않았습니다. L1, L2가 완성된 후에 구현 예정입니다.

---

## 추가 리소스

- [API Reference](./API_REFERENCE.md)
- [레이어 구조 다이어그램](./LAYER_ARCHITECTURE_DIAGRAM.md)
- [전체 레이어 구조 분석](./LAYER_ARCHITECTURE_ANALYSIS.md)

---

**작성자**: GNJz (Qquarts)  
**최종 업데이트**: 2026-02-03

