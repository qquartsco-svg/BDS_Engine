# Unsolved Problems Engines

> **난제 해결 엔진 모듈 모음**  
> **Collection of Unsolved Problems Analysis Engines**

---

## 🎯 목적

이 폴더는 **"난제를 다르게 말할 수 있는 도구"** 모음입니다.

### 핵심 철학

**우리가 하지 않는 것**:
- ❌ 난제를 "증명"하기
- ❌ "정답"을 제시하기
- ❌ 해석적 해 도출

**우리가 하는 것**:
- ✅ 난제를 "다르게 말하기"
- ✅ 원인 구조 분석
- ✅ 동역학적 재서술
- ✅ 경계 정합 관점에서 재해석

---

## 📁 엔진 모듈 목록

### UP-1: ThreeBodyBoundaryEngine

**삼체 문제 경계 정합 분석 엔진**

- 위치: `ThreeBodyBoundaryEngine/`
- 역할: 삼체 궤도 정합 분석을 통한 원인 구조 분석
- 핵심 질문: "왜 특정 지점에서 궤도가 붕괴하는가?"

**문서**: [ThreeBodyBoundaryEngine README](./ThreeBodyBoundaryEngine/README.md)

---

## 🏗️ 폴더 구조

```
Unsolved_Problems_Engines/
├── README.md (이 파일)
├── ThreeBodyBoundaryEngine/
│   ├── src/
│   │   └── three_body_boundary_engine/
│   ├── docs/
│   ├── examples/
│   ├── tests/
│   ├── setup.py
│   ├── requirements.txt
│   └── README.md
└── (향후 추가 엔진들...)
```

---

## 🚀 사용 방법

### 독립 모듈로 사용

각 엔진은 완전히 독립적으로 작동합니다:

```python
# ThreeBodyBoundaryEngine 예시
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodyConfig
)

config = ThreeBodyConfig()
engine = ThreeBodyBoundaryEngine(config)
# ... 사용 ...
```

### BDS Engine과 통합

```python
from cognitive_kernel import CognitiveKernel
from three_body_boundary_engine import ThreeBodyBoundaryEngine

kernel = CognitiveKernel()
kernel.add_engine(ThreeBodyBoundaryEngine())
```

---

## 📊 적용 가능한 난제

1. **삼체 문제** (Three-Body Problem) - ✅ 구현됨
2. **나비에-스토크스** (Navier-Stokes) - 🔄 예정
3. **카오스** (Chaos Theory) - 🔄 예정
4. **양자-고전 경계** (Quantum-Classical Boundary) - 🔄 예정

---

## 🔗 관련 문서

- [난제 해결 엔진 모듈 프레임워크](../UNSOLVED_PROBLEMS_ENGINE_FRAMEWORK.md)
- [엔진 모듈 상세 분석](../ENGINE_MODULE_ANALYSIS.md)
- [구현 로드맵](../IMPLEMENTATION_ROADMAP.md)

---

**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0

