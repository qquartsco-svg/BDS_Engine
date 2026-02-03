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

## 📊 주요 기능

### 1. 궤도 안정성 분석

```python
analysis = engine.analyze_orbit_stability(system)

# 원인 분석:
# - "왜 특정 조건에서 궤도가 안정/불안정한가?"
# - 경계 정합 실패 메커니즘 규명
```

### 2. 경계 형성 과정 관찰

```python
time_steps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
dynamics = engine.observe_boundary_formation(system, time_steps)

# 원인 분석:
# - "경계가 시간에 따라 어떻게 변하는가?"
# - 붕괴 시점 식별
collapse_point = dynamics.get_collapse_point()
```

### 3. 라그랑주 점 경계 관찰

```python
lagrange_analysis = engine.observe_lagrange_points(system)

# 원인 분석:
# - "라그랑주 점에서 경계 형성이 어떻게 다른가?"
# - 안정/불안정 라그랑주 점 구분
for lp in lagrange_analysis.lagrange_points:
    print(f"{lp.lagrange_type}: {lp.stability}")
```

### 4. 안정/불안정 조건 비교

```python
# 다양한 초기 조건
systems = [system1, system2, system3]
results = engine.compare_stability_conditions(systems)

# 원인 분석:
# - "어떤 초기 조건이 안정/불안정한가?"
# - 안정성 패턴 식별
```

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

- [API Reference](./docs/API_REFERENCE.md)
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

**Version**: 1.1.0 (원인 분석 전용)  
**Last Updated**: 2026-02-02

### 버전 히스토리

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
**Version**: 1.1.0 (Causal Analysis Only)

