# 해결 접근법 파일 위치 가이드

**작성일**: 2026-02-02  
**목적**: 해결 접근법 관련 파일 위치 안내

---

## 📁 해결 접근법 파일 위치

### 절대 경로 (기준)
```
/Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/
Unsolved_Problems_Engines/ThreeBodyBoundaryEngine/
```

---

## 💻 소스 코드 파일

### 1. 메인 엔진 (해결 메서드 포함)
**파일**: `src/three_body_boundary_engine/three_body_boundary_engine.py`

**절대 경로**:
```
/Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/
Unsolved_Problems_Engines/ThreeBodyBoundaryEngine/
src/three_body_boundary_engine/three_body_boundary_engine.py
```

**포함된 해결 메서드**:
- `recover_boundary_alignment()` (라인 ~300-400)
- `stabilize_system()` (라인 ~400-500)
- `apply_dynamic_correction()` (라인 ~500-600)

**빠른 접근**:
```bash
cd /Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines/ThreeBodyBoundaryEngine
cat src/three_body_boundary_engine/three_body_boundary_engine.py | grep -A 20 "def recover_boundary_alignment"
```

---

### 2. 데이터 모델 (해결 결과 클래스)
**파일**: `src/three_body_boundary_engine/models.py`

**절대 경로**:
```
/Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/
Unsolved_Problems_Engines/ThreeBodyBoundaryEngine/
src/three_body_boundary_engine/models.py
```

**포함된 클래스**:
- `RecoveryResult` (경계 정합 복구 결과)
- `StabilizationResult` (안정화 결과)
- `CorrectionResult` (동적 보정 결과)

**빠른 접근**:
```bash
cd /Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines/ThreeBodyBoundaryEngine
grep -A 10 "class RecoveryResult" src/three_body_boundary_engine/models.py
```

---

## 📝 문서 파일

### 1. 해결 접근법 설계 문서
**파일**: `docs/SOLUTION_APPROACH.md`

**절대 경로**:
```
/Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/
Unsolved_Problems_Engines/ThreeBodyBoundaryEngine/
docs/SOLUTION_APPROACH.md
```

**내용**:
- 철학적 전환 (원인 분석 → 해결)
- 해결 접근의 핵심 (경계 정합 복구, 안정화 메커니즘, 동적 보정)
- 수학적 기반
- 구현 계획

**빠른 접근**:
```bash
cd /Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines/ThreeBodyBoundaryEngine
cat docs/SOLUTION_APPROACH.md
```

---

## 📚 예제 파일

### 1. 해결 접근법 사용 예제
**파일**: `examples/solution_example.py`

**절대 경로**:
```
/Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/
Unsolved_Problems_Engines/ThreeBodyBoundaryEngine/
examples/solution_example.py
```

**내용**:
- 경계 정합 복구 예제
- 안정화 메커니즘 예제
- 동적 보정 예제
- 종합 결과 분석

**실행**:
```bash
cd /Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines/ThreeBodyBoundaryEngine
python3 examples/solution_example.py
```

---

## 🔍 파일 찾기 명령어

### 모든 해결 관련 파일 찾기
```bash
cd /Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines/ThreeBodyBoundaryEngine
find . -type f -name "*solution*" -o -name "*recover*" -o -name "*stabilize*" -o -name "*correction*"
```

### 해결 메서드 검색
```bash
cd /Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines/ThreeBodyBoundaryEngine
grep -n "def recover_boundary_alignment\|def stabilize_system\|def apply_dynamic_correction" src/three_body_boundary_engine/three_body_boundary_engine.py
```

### 해결 결과 클래스 검색
```bash
cd /Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines/ThreeBodyBoundaryEngine
grep -n "class RecoveryResult\|class StabilizationResult\|class CorrectionResult" src/three_body_boundary_engine/models.py
```

---

## 📊 파일 구조 요약

```
ThreeBodyBoundaryEngine/
├── src/
│   └── three_body_boundary_engine/
│       ├── three_body_boundary_engine.py  ← 해결 메서드 (3개)
│       └── models.py                      ← 해결 결과 클래스 (3개)
├── docs/
│   └── SOLUTION_APPROACH.md               ← 해결 접근법 문서
└── examples/
    └── solution_example.py                ← 해결 접근법 예제
```

---

## 🚀 빠른 접근

### Python에서 import
```python
import sys
from pathlib import Path

# 프로젝트 루트 추가
project_root = Path("/Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines/ThreeBodyBoundaryEngine")
sys.path.insert(0, str(project_root / "src"))

# 해결 메서드 사용
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    RecoveryResult,
    StabilizationResult,
    CorrectionResult
)

engine = ThreeBodyBoundaryEngine()
recovery = engine.recover_boundary_alignment(system)
stabilization = engine.stabilize_system(system)
correction = engine.apply_dynamic_correction(system, time_steps)
```

---

**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0

