# BDS Engine (Brain Disorder Simulation Engine)

> **뇌 질환 시뮬레이션 엔진**  
> **Brain Disorder Simulation Engine**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**BDS Engine**은 뇌 질환을 시뮬레이션하고 인지 동역학을 모델링하는 통합 엔진 프레임워크입니다.

> **🇰🇷 한국어** (기본) | [🇺🇸 English Version](#english-version)

---

## 🎯 프로젝트 개요

BDS Engine은 여러 개의 독립적이면서도 상호 연동 가능한 인지/뇌질환 시뮬레이션 엔진들로 구성된 프레임워크입니다. 다양한 뇌 질환(ADHD, ASD, PTSD, 치매, 알츠하이머 등)을 물리학적 동역학으로 모델링합니다.

### 핵심 철학

> **이 프로젝트의 헌법**

- **질환 = 고장이 아니라 상태공간 상의 궤도**
- **기억 = 저장된 데이터가 아니라 동역학을 되돌리는 힘**
- **인지 = 엔트로피-회전-코어 기반 동역학 시스템**

---

## 🔧 포함된 엔진

### 1. Boundary Convergence Engine (9번)

**경계-공간 정합 계수 엔진**

BDS Engine 내에서 형태 형성과 경계 안정화를 담당하는 핵심 엔진입니다.

- 경계와 공간의 정합 과정을 동역학적으로 모델링
- π의 수렴 과정을 경계-공간 정합으로 재해석
- 인지 공간 형성 시뮬레이션

> ⚠️ **중요 명확화**: Boundary Convergence Engine은 **π(원주율)를 계산하거나 근사하는 수학 엔진이 아닙니다**.  
> 본 엔진은 경계(boundary)와 내부 공간(space)이 상호작용하며 형태가 안정화되는 **동역학적 과정**을 시뮬레이션합니다.

**위치**: [`Boundary_Convergence_Engine/`](./Boundary_Convergence_Engine/)

**자세한 설명**: [Boundary Convergence Engine README](./Boundary_Convergence_Engine/README.md)

---

## 📚 주요 기능

### 1. 인지 동역학 모델링
- 엔트로피 기반 탐색
- 코어 강도 수렴
- 회전 동역학 (Precession)

### 2. 경계-공간 정합
- 경계 생성 및 정제
- 밀도 추정
- 수렴 동역학

### 3. 뇌 질환 시뮬레이션
- ADHD (고엔트로피, 강한 회전)
- ASD (저엔트로피, 약한 회전)
- 치매/알츠하이머 (코어 붕괴)

---

## 🚀 빠른 시작

### Boundary Convergence Engine 사용

```python
from boundary_convergence_engine import (
    BoundaryConvergenceEngine,
    BoundaryConvergenceConfig
)

# 엔진 생성
config = BoundaryConvergenceConfig()
engine = BoundaryConvergenceEngine(config)

# 수렴 실행
result = engine.converge()

# 결과 확인
print(f"수렴 완료: {result.converged}")
print(f"최종 불일치: {result.mismatch}")
print(f"경계 점 개수: {result.boundary_points}")
```

자세한 사용법: [Boundary Convergence Engine 사용 예제](./Boundary_Convergence_Engine/USAGE_EXAMPLES.md)

---

## 📖 문서

### 엔진별 문서
- [Boundary Convergence Engine](./Boundary_Convergence_Engine/README.md) - 경계-공간 정합 엔진
- [Boundary Convergence Engine 연계 가이드](./Boundary_Convergence_Engine/INTEGRATION_WITH_DYNAMICS.md) - Dynamics Engine과의 연계

### 개념 문서
- [공간 채움 동역학](../../Cognitive_Kernel/docs/SPACE_FILLING_DYNAMICS.md)
- [Boundary Convergence Engine 설계](../../Cognitive_Kernel/docs/BOUNDARY_CONVERGENCE_ENGINE_DESIGN.md)

---

## 🔗 관련 프로젝트

- [Cognitive Kernel](https://github.com/gnjz/cognitive-kernel) - 인지 커널
- [Dynamics Engine](https://pypi.org/project/dynamics-engine/) - 동역학 엔진 (PyPI)
- [Boundary Convergence Engine](https://pypi.org/project/boundary-convergence-engine/) - 경계 수렴 엔진 (PyPI)

---

## 🔐 PHAM 블록체인

모든 엔진은 PHAM (Proof of Authorship & Merit) 블록체인 시스템으로 서명되어 있습니다.

- **Boundary Convergence Engine**: [PHAM_BLOCKCHAIN_LOG.md](./Boundary_Convergence_Engine/PHAM_BLOCKCHAIN_LOG.md)

---

## ⚠️ 면책 조항 및 오해 방지

### 의료 관련 면책

이 패키지는:
- ✅ 연구/교육 목적
- ✅ 메커니즘 탐색 도구
- ✅ 패턴 관측 시스템

이 패키지는 아닙니다:
- ❌ 진단 도구
- ❌ 치료 솔루션
- ❌ 의료기기
- ❌ 임상 의사결정 보조

### 기술적 오해 방지

**Boundary Convergence Engine 관련**:
- ❌ π(원주율) 계산 엔진이 아님
- ❌ 수학적 근사 알고리즘이 아님
- ❌ 원 근사 도구가 아님
- ✅ 경계-공간 상호작용의 동역학적 시뮬레이션 엔진

---

## 📄 라이선스

MIT License

---

## 👤 작성자

GNJz (Qquarts)

---

## 📝 버전

**Version**: 1.0.0  
**Last Updated**: 2026-02-02

---

## English Version

### BDS Engine (Brain Disorder Simulation Engine)

**BDS Engine** is an integrated engine framework for simulating brain disorders and modeling cognitive dynamics.

### Included Engines

BDS Engine is a framework composed of multiple independent yet interoperable cognitive/brain disorder simulation engines. Boundary Convergence Engine is a core engine responsible for form formation and boundary stabilization.

#### 1. Boundary Convergence Engine (No. 9)

**Boundary-Space Alignment Coefficient Engine**

- Dynamically models the alignment process between boundaries and space
- Reinterprets π convergence as boundary-space alignment
- Simulates cognitive space formation

> ⚠️ **Important Clarification**: Boundary Convergence Engine does **NOT** compute or approximate π numerically.  
> It simulates the dynamical process by which boundaries and interior space interact and stabilize into coherent forms.

**Location**: [`Boundary_Convergence_Engine/`](./Boundary_Convergence_Engine/)

**Detailed Documentation**: [Boundary Convergence Engine README](./Boundary_Convergence_Engine/README.md)

### Key Features

1. **Cognitive Dynamics Modeling**
   - Entropy-based exploration
   - Core strength convergence
   - Rotational dynamics (Precession)

2. **Boundary-Space Alignment**
   - Boundary generation and refinement
   - Density estimation
   - Convergence dynamics

3. **Brain Disorder Simulation**
   - ADHD (High entropy, strong rotation)
   - ASD (Low entropy, weak rotation)
   - Dementia/Alzheimer's (Core collapse)

### Quick Start

```python
from boundary_convergence_engine import (
    BoundaryConvergenceEngine,
    BoundaryConvergenceConfig
)

config = BoundaryConvergenceConfig()
engine = BoundaryConvergenceEngine(config)
result = engine.converge()

print(f"Converged: {result.converged}")
print(f"Final Mismatch: {result.mismatch}")
```

> ⚠️ **Important Clarification**: Boundary Convergence Engine does **NOT** compute or approximate π numerically.  
> It simulates the dynamical process by which boundaries and interior space interact and stabilize into coherent forms.

### Documentation

- [Boundary Convergence Engine](./Boundary_Convergence_Engine/README.md)
- [Integration Guide](./Boundary_Convergence_Engine/INTEGRATION_WITH_DYNAMICS.md)

### Related Projects

- [Cognitive Kernel](https://github.com/gnjz/cognitive-kernel)
- [Dynamics Engine](https://pypi.org/project/dynamics-engine/)
- [Boundary Convergence Engine](https://pypi.org/project/boundary-convergence-engine/)

### PHAM Blockchain

All engines are signed with PHAM (Proof of Authorship & Merit) blockchain system.

- **Boundary Convergence Engine**: [PHAM_BLOCKCHAIN_LOG.md](./Boundary_Convergence_Engine/PHAM_BLOCKCHAIN_LOG.md)

---

**Author**: GNJz (Qquarts)  
**Version**: 1.0.0
