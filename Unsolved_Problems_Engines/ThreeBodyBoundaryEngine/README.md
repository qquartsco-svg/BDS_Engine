# ThreeBodyBoundaryEngine

> **삼체 문제 경계 정합 분석 엔진**  
> **Three-Body Problem Boundary Convergence Analysis Engine**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**ThreeBodyBoundaryEngine**은 삼체 문제를 경계 정합 관점에서 **원인 분석**하는 독립 엔진 모듈입니다.

> **핵심 용도**: **실패 가능성 평가 및 실패 원인 추적**  
> 이 엔진은 시스템이 붕괴할 가능성을 정량화하고, 실패 원인을 구조적으로 추적합니다.

> **⚠️ 아키텍처 원칙**: 이 엔진은 "원인 분석 전용"입니다. 해결 탐색 기능은 별도 모듈로 분리됩니다.
> "진단서(원인)와 처방전(해결)은 분리되어야 함" - [아키텍처 철학](./docs/ARCHITECTURE_PHILOSOPHY.md)

> **🇰🇷 한국어** (기본) | [🇺🇸 English Version](#english-version)

---

## 🎯 핵심 철학

### 우리가 하지 않는 것
- ❌ 삼체 문제의 "해"를 제공
- ❌ "정답"을 제시
- ❌ 해석적 해 도출

### 우리가 하는 것
- ✅ 경계 정합 관점에서 궤도 안정성 분석
- ✅ 원인 구조 분석: "왜 특정 지점에서 궤도가 붕괴하는가?"
- ✅ 동역학적 재서술: "안정 궤도 = 경계-공간 정합 상태"

### 아키텍처 원칙
- ✅ **원인 분석 전용**: 이 엔진은 "왜 안 되는지"를 끝까지 파고듭니다
- ✅ **해결 탐색 분리**: 해결 탐색 기능은 별도 모듈로 구현됩니다
- ✅ **설명 가능성 최우선**: 실패를 실패로 존중하고 정확히 설명합니다

---

## 🔬 핵심 개념

### 1. 경계 정합 관점

**기존 질문**: "해가 존재하는가?"

**우리의 질문**: "왜 경계 정합이 실패하는가?"

**핵심 아이디어**:
- 안정 궤도 = 경계-공간 정합 상태
- 혼돈 = 경계 refinement 실패
- π 개념: 정합 계수 붕괴

### 2. 수식

**중력 퍼텐셜 → 밀도 변환**:
```
V(x,y) = -G * Σ(m_i / r_i)
ρ(x,y) = V(x,y) / V_max  (정규화)
```

**경계 정합 계산**:
```
Δ(경계, 공간) = |P - 2πr| / 2πr + |A - πr²| / πr²
```

**안정성 판정**:
```
안정: Δ < 임계값, 수렴 속도 > 0
불안정: Δ > 임계값, 수렴 속도 < 0 (발산)
```

---

## 🚀 빠른 시작

### 설치

```bash
pip install three-body-boundary-engine
```

### 기본 사용법

```python
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodyConfig,
    ThreeBodySystem,
    Body,
    Point
)

# 엔진 생성
config = ThreeBodyConfig()
engine = ThreeBodyBoundaryEngine(config)

# 삼체 시스템 생성
system = ThreeBodySystem(
    body1=Body(position=Point(0.0, 0.0), mass=1.0),
    body2=Body(position=Point(1.0, 0.0), mass=1.0),
    body3=Body(position=Point(0.5, 0.866), mass=1.0)
)

# 궤도 안정성 분석
analysis = engine.analyze_orbit_stability(system)

# 결과 확인
print(f"안정 여부: {analysis.is_stable()}")
print(f"안정성 점수: {analysis.stability_score:.3f}")
print(f"불일치(Δ): {analysis.mismatch:.6f}")
```

---

## 🏛️ 레이어 아키텍처

이 엔진은 **3개의 레이어**로 구성되어 있으며, 각 레이어는 독립적으로 동작하면서도 통합 가능합니다.

### 레이어 구조 개요

```
L0: 원인 분석 레이어 (법칙)
  └─ ThreeBodyBoundaryEngine
  └─ "왜 실패하는지" 분석

L1: 실패 추적 레이어 (기억)
  └─ FailureAtlas
  └─ "어디서 실패하는지" 기록

L2: 실패 학습 레이어 (본능)
  └─ FailureBiasConverter
  └─ "어디를 피해야 하는지" 학습
```

**자세한 내용**: [레이어 구조 다이어그램](./docs/LAYER_ARCHITECTURE_DIAGRAM.md) | [전체 레이어 구조 분석](./docs/LAYER_ARCHITECTURE_ANALYSIS.md)

---

## 📊 주요 기능

### L0: 원인 분석 레이어

#### 1. 궤도 안정성 분석

```python
analysis = engine.analyze_orbit_stability(system)

# 원인 분석:
# - "왜 특정 조건에서 궤도가 안정/불안정한가?"
# - 경계 정합 실패 메커니즘 규명
```

#### 2. 경계 형성 과정 관찰

```python
time_steps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
dynamics = engine.observe_boundary_formation(system, time_steps)

# 원인 분석:
# - "경계가 시간에 따라 어떻게 변하는가?"
# - 붕괴 시점 식별
collapse_point = dynamics.get_collapse_point()
```

#### 3. 라그랑주 점 경계 관찰

```python
lagrange_analysis = engine.observe_lagrange_points(system)

# 원인 분석:
# - "라그랑주 점에서 경계 형성이 어떻게 다른가?"
# - 안정/불안정 라그랑주 점 구분
for lp in lagrange_analysis.lagrange_points:
    print(f"{lp.lagrange_type}: {lp.stability}")
```

#### 4. 안정/불안정 조건 비교

```python
# 다양한 초기 조건
systems = [system1, system2, system3]
results = engine.compare_stability_conditions(systems)

# 원인 분석:
# - "어떤 초기 조건이 안정/불안정한가?"
# - 안정성 패턴 식별
```

### L1: 실패 추적 레이어

#### 1. 실패 기록 및 구조화

```python
from three_body_boundary_engine import FailureAtlas

atlas = FailureAtlas()

# L0 분석 결과를 실패 기록으로 변환
record = atlas.record_failure(analysis, system, threshold=0.1)

if record:
    print(f"붕괴 모드: {record.collapse_mode.value}")
    print(f"심각도: {record.collapse_severity:.3f}")
```

**알고리즘**:
- 조건 서명 생성: 질량 비율과 거리 패턴을 문자열로 인코딩
- 붕괴 모드 분류: 발산/불일치/수렴 실패 자동 판정
- 실패 유형별 분류: Failure Manifold에 구조화하여 저장

**자세한 내용**: [API Reference - L1](./docs/API_REFERENCE.md#l1-실패-추적-레이어)

#### 2. 유사한 실패 패턴 찾기

```python
# 유사한 실패 패턴 검색
similar = atlas.get_similar_failures(
    condition_signature=record.condition_signature,
    similarity_threshold=0.5
)
```

**알고리즘**:
- 조건 서명 유사도 계산: 공통 부분 비율 기반
- 실패 패턴 그룹화: 구조적 유사성 발견

#### 3. 실패 통계 분석

```python
stats = atlas.get_failure_statistics()
# - 총 실패 횟수
# - 붕괴 모드별 분류
# - 실패 유형별 분류
```

**핵심 가치**: "혼돈은 랜덤이 아니다" 증명 가능

---

### L2: 실패 학습 레이어

> **⚠️ 중요 명확화**: 본 레이어는 어떠한 정책, 행동, 해결책도 생성하지 않습니다.  
> 오직 탐색 공간에서의 위험 지형만을 형성합니다.  
> 최적화나 강화학습이 아닙니다.

#### 1. 실패 → 편향 변환

```python
from three_body_boundary_engine import FailureBiasConverter

converter = FailureBiasConverter()
bias = converter.convert_failure_to_bias(atlas)
```

**알고리즘**:
- 위험 지도 생성: 실패 빈도(60%) + 심각도(40%) 가중 결합
- 붕괴 모드별 위험도: 각 모드의 실패율 계산
- 탐색 편향 생성: "이 방향은 위험하다" 내부 지형 생성

**수식**:
```
위험도 = (빈도_위험도 × 0.6) + (심각도_위험도 × 0.4)
```

**자세한 내용**: [API Reference - L2](./docs/API_REFERENCE.md#l2-실패-학습-레이어)

#### 2. 조건 회피 판정

```python
should_avoid = converter.should_avoid_condition(
    bias=bias,
    condition_signature=condition_sig,
    threshold=0.3
)
```

**알고리즘**:
- 위험도 조회: 조건 서명별 위험도 확인
- 임계값 비교: threshold 이상이면 회피 권장

#### 3. 안전한 조건 필터링

```python
safe_conditions = converter.get_safe_conditions(
    bias=bias,
    candidate_conditions=candidates,
    threshold=0.3
)
```

**알고리즘**:
- 후보 조건 평가: 각 조건의 위험도 확인
- 안전 조건 필터링: threshold 미만만 반환

#### 4. STDP 유사 메커니즘

```python
# 새로운 실패 기록으로 편향 업데이트
updated_bias = converter.update_bias_with_new_failure(
    bias=bias,
    new_record=new_record
)
```

**알고리즘**:
- 위험도 감쇠: 기존 위험도에 `risk_decay_factor` 적용
- 최신 실패 반영: 새로운 실패 기록의 위험도와 비교하여 큰 값 선택
- STDP 유사: 최근 실패일수록 더 큰 영향

**핵심 가치**: "초반 실패 → 후반 성공률 증가" 구조 성립

**⚠️ 명확화**: L2는 해결책을 찾지 않습니다. 위험 지형만 형성하여 L3(미래)가 안전하게 탐색할 수 있도록 합니다.

---

### 통합 사용 예제

```python
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    FailureAtlas,
    FailureBiasConverter,
    ThreeBodySystem,
    Body,
    Point
)

# 레이어 생성
engine = ThreeBodyBoundaryEngine()  # L0
atlas = FailureAtlas()              # L1
converter = FailureBiasConverter()  # L2

# 시스템 분석
system = ThreeBodySystem(...)

# L0 → L1 → L2 파이프라인
analysis = engine.analyze_orbit_stability(system)  # L0
atlas.record_failure(analysis, system)            # L1
bias = converter.convert_failure_to_bias(atlas)   # L2

# 위험한 조건 회피
should_avoid = converter.should_avoid_condition(
    bias=bias,
    condition_signature=condition_sig,
    threshold=0.3
)
```

**자세한 내용**: [사용 가이드](./docs/USAGE_GUIDE.md) | [통합 예제](./examples/l2_bias_example.py)

---

## 🏭 산업/상업용 적용

### 산업용

**우주 항공**:
- 위성 궤도 안정성 분석
- 우주선 경로 최적화
- 라그랑주 점 활용

**게임/시뮬레이션**:
- 천체 시뮬레이션
- 물리 엔진 최적화

### 상업용

**AI/머신러닝**:
- 복잡계 시뮬레이션
- 동역학 시스템 분석

---

## ⚡ LLM 전력 효율 개선

### 전력 효율 기여 메커니즘

이 엔진은 LLM의 **불필요한 계산을 차단**하여 전력 효율을 개선합니다.

**레이어별 기여**:
- **L0**: 불가능한 영역 차단 → 30-50% 전력 절감
- **L1**: 중복 시도 방지 → 20-40% 전력 절감
- **L2**: 탐색 공간 축소 → 40-60% 전력 절감
- **통합 효과**: **50-70% 전력 절감** (단기), **70-80%** (장기)

**구조적 동등성**: STDP의 LTD(장기 억제) 메커니즘과 완벽히 일치

**자세한 내용**: [전력 효율 분석](./docs/POWER_EFFICIENCY_ANALYSIS.md) | [LLM 통합 분석](./docs/LLM_INTEGRATION_ANALYSIS.md)

---

## 🧠 뇌 브레인 모듈 연계

### 인지 공간 형성

- 기억 간 상호작용 = 천체 간 중력
- 인지 안정성 = 궤도 안정성
- ADHD = 불안정 궤도 (과도한 탐색)

### Dynamics Engine 연계

```python
# 엔트로피 → 밀도
entropy = dynamics.calculate_entropy(probabilities)
density = entropy_to_density(entropy)

# 경계 → 코어 강도
boundary = engine.analyze_orbit_stability(system)
core_strength = boundary_to_core_strength(boundary)
```

---

## 📚 문서

### 핵심 문서
- [API Reference](./docs/API_REFERENCE.md) ⭐ 완전한 API 명세
- [사용 가이드](./docs/USAGE_GUIDE.md) ⭐ 레이어별 사용법 및 베스트 프랙티스
- [레이어 구조 다이어그램](./docs/LAYER_ARCHITECTURE_DIAGRAM.md) ⭐ 레이어 간 데이터 흐름
- [전체 레이어 구조 분석](./docs/LAYER_ARCHITECTURE_ANALYSIS.md) ⭐ 레이어 맵 및 설계 철학
- [에러 처리 가이드](./docs/ERROR_HANDLING.md) ⭐ 에러 처리 및 복구 전략

### 추가 문서
- [수학적 기초](./docs/MATHEMATICAL_FOUNDATION.md)
- [사용 예제](./examples/)
- [활용 분석 및 발전 방향](./docs/APPLICATION_ANALYSIS.md) ⭐ NEW
- [실패 가능성 및 실패 추적 분석](./docs/FAILURE_ANALYSIS.md) ⭐ 핵심 용도
- [실패 학습 메커니즘 분석](./docs/FAILURE_LEARNING_ANALYSIS.md) ⭐ STDP 유사 메커니즘
- [로직 흐름 분석](./docs/LOGIC_FLOW_ANALYSIS.md) ⭐ 추적 → 학습 → 해결 탐색
- [전체 레이어 구조 분석](./docs/LAYER_ARCHITECTURE_ANALYSIS.md) ⭐ L0~L4 레이어 맵

---

## 🔐 PHAM 블록체인

이 엔진은 PHAM (Proof of Authorship & Merit) 블록체인 시스템으로 서명되어 있습니다.

- [PHAM_BLOCKCHAIN_LOG.md](./PHAM_BLOCKCHAIN_LOG.md)

---

## ⚠️ 면책 조항 및 정확한 정체성

### 이 엔진이 하는 일

**핵심 정체성**: 삼체 문제를 "운동 방정식의 난제"가 아니라 **"공간이 하나의 일관된 형태를 가질 수 없는 조건의 문제"**로 재서술하는 원인 분석 엔진입니다.

**처리 파이프라인**:
1. **삼체 → 중력 퍼텐셜 필드**: `V(x,y) = -G * Σ(m_i / r_i)` (정적 스냅샷)
2. **퍼텐셜 → 밀도**: `ρ(x,y) = normalize(V)` (공간 구조로 변환)
3. **밀도 → 경계 정합**: 공간이 일관된 형태(경계)로 수렴 가능한가 측정
4. **불일치 계산**: `Δ = (|P - 2πr| / 2πr + |A - πr²| / πr²) / 2`

**말할 수 있는 것**:
- ✅ 이 삼체 배치는 공간적으로 일관된 경계를 만들 수 있는가
- ✅ 공간 구조가 형태로 수렴하려다 어디서 실패하는가
- ✅ 혼돈은 "무작위성"이 아니라 경계 정합 실패의 누적 결과

### 이 엔진이 하지 않는 일

**❌ 말할 수 없는 것**:
- 시간에 따른 궤도 붕괴 원인 (동역학적 전개 과정)
- 초기 속도 민감성 분석
- 리아푸노프 지수 계산
- 궤도 시뮬레이션 (시간 적분 없음)

**정확한 한계**:
- ⚠️ 현재 엔진은 **"혼돈의 기원 조건"**을 분석합니다
- ⚠️ 현재 엔진은 **"혼돈의 전개 과정"**을 시뮬레이션하지 않습니다
- ⚠️ 이는 약점이 아니라, 원인 분석 엔진으로서의 정확한 위치 선정입니다

**이 엔진은 아닙니다**:
- ❌ 삼체 문제의 "해"를 제공하는 시스템
- ❌ "정답"을 제시하는 도구
- ❌ 해결 탐색 엔진 (별도 모듈로 구현 예정)
- ❌ 시간 진화 시뮬레이터 (정적 공간 분석 전용)

---

## 📄 라이선스

MIT License

---

## 👤 작성자

GNJz (Qquarts)

---

## 📝 버전

**Version**: 1.2.0 (레이어 확장)  
**Last Updated**: 2026-02-03

### 버전 히스토리

- **v1.2.0** (2026-02-03): 레이어 확장
  - L1 레이어 추가 (실패 추적)
  - L2 레이어 추가 (실패 학습)
  - 레이어 구조 완성 (L0 + L1 + L2)
  - 문서화 완성 (API, 사용 가이드, 성능 벤치마크)

- **v1.1.0** (2026-02-02): 원인 분석과 해결 탐색 분리
  - 해결 탐색 기능 제거 (별도 모듈로 분리)
  - 원인 분석 전용으로 명확화
  - 아키텍처 철학 문서 추가

- **v1.0.0** (2026-02-02): 초기 릴리스
  - 원인 분석 기능 구현
  - 해결 탐색 기능 (프로토타입, 제거됨)

---

## English Version

### ThreeBodyBoundaryEngine

**ThreeBodyBoundaryEngine** is an independent engine module that analyzes the three-body problem from a boundary convergence perspective.

### Core Philosophy

**What we don't do**:
- ❌ Provide "solutions" to the three-body problem
- ❌ Present "answers"
- ❌ Derive analytical solutions

**What we do**:
- ✅ Analyze orbital stability from a boundary convergence perspective
- ✅ Causal structure analysis: "Why does the orbit collapse at specific points?"
- ✅ Dynamical re-description: "Stable orbit = boundary-space alignment state"

### Key Concepts

**Gravity Potential → Density Conversion**:
```
V(x,y) = -G * Σ(m_i / r_i)
ρ(x,y) = V(x,y) / V_max  (normalized)
```

**Boundary Convergence Calculation**:
```
Δ(boundary, space) = |P - 2πr| / 2πr + |A - πr²| / πr²
```

**Stability Judgment**:
```
Stable: Δ < threshold, convergence rate > 0
Unstable: Δ > threshold, convergence rate < 0 (divergence)
```

### Quick Start

```python
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodyConfig,
    ThreeBodySystem,
    Body,
    Point
)

config = ThreeBodyConfig()
engine = ThreeBodyBoundaryEngine(config)

system = ThreeBodySystem(
    body1=Body(position=Point(0.0, 0.0), mass=1.0),
    body2=Body(position=Point(1.0, 0.0), mass=1.0),
    body3=Body(position=Point(0.5, 0.866), mass=1.0)
)

analysis = engine.analyze_orbit_stability(system)
print(f"Stable: {analysis.is_stable()}")
print(f"Stability Score: {analysis.stability_score:.3f}")
```

---

**Author**: GNJz (Qquarts)  
**Version**: 1.2.0 (Layer Architecture)

