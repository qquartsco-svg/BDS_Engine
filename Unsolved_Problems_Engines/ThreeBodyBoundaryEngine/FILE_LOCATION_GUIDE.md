# 파일 위치 가이드

**작성일**: 2026-02-02  
**목적**: ThreeBodyBoundaryEngine의 모든 파일 위치 안내

---

## 📁 전체 폴더 구조

```
Unsolved_Problems_Engines/
└── ThreeBodyBoundaryEngine/
    ├── src/
    │   └── three_body_boundary_engine/
    │       ├── __init__.py
    │       ├── three_body_boundary_engine.py (메인 엔진)
    │       ├── config.py (설정)
    │       ├── models.py (데이터 모델)
    │       ├── point.py (Point 클래스)
    │       ├── gravity_calculator.py (중력 계산)
    │       ├── boundary_convergence_adapter.py (경계 수렴)
    │       └── lagrange_calculator.py (라그랑주 점)
    ├── docs/ (문서 폴더)
    ├── examples/
    │   └── basic_usage.py (기본 사용 예제)
    ├── tests/
    │   ├── __init__.py
    │   ├── test_three_body_boundary_engine.py (기본 테스트)
    │   ├── test_gravity_calculator.py (중력 계산기 테스트)
    │   ├── test_boundary_convergence.py (경계 수렴 테스트)
    │   ├── test_integration.py (통합 테스트)
    │   └── run_all_tests.py (전체 테스트 실행)
    ├── README.md (메인 문서)
    ├── LICENSE (라이선스)
    ├── PHAM_BLOCKCHAIN_LOG.md (블록체인 해시 기록)
    ├── setup.py (패키지 설정)
    ├── requirements.txt (의존성)
    └── .gitignore

Unsolved_Problems_Engines/
└── UP-2_BoundarySafeSearchEngine/
    ├── docs/
    │   └── UP-2_DESIGN.md (L3 설계 문서, 구현 대기)
    ├── examples/ (향후)
    ├── src/ (향후)
    ├── tests/ (향후)
    └── README.md (UP-2 개요)
```

---

## 📄 주요 파일 위치

### 소스 코드

| 파일 | 경로 |
|------|------|
| 메인 엔진 | `src/three_body_boundary_engine/three_body_boundary_engine.py` |
| 설정 | `src/three_body_boundary_engine/config.py` |
| 데이터 모델 | `src/three_body_boundary_engine/models.py` |
| Point 클래스 | `src/three_body_boundary_engine/point.py` |
| 중력 계산기 | `src/three_body_boundary_engine/gravity_calculator.py` |
| 경계 수렴 어댑터 | `src/three_body_boundary_engine/boundary_convergence_adapter.py` |
| 라그랑주 점 계산기 | `src/three_body_boundary_engine/lagrange_calculator.py` |
| 패키지 초기화 | `src/three_body_boundary_engine/__init__.py` |

### 문서

| 파일 | 경로 |
|------|------|
| 메인 README | `README.md` |
| 블록체인 로그 | `PHAM_BLOCKCHAIN_LOG.md` |
| 파일 위치 가이드 | `FILE_LOCATION_GUIDE.md` (이 파일) |

### 예제 및 테스트

| 파일 | 경로 |
|------|------|
| 기본 사용 예제 | `examples/basic_usage.py` |
| 기본 테스트 | `tests/test_three_body_boundary_engine.py` |
| 중력 계산기 테스트 | `tests/test_gravity_calculator.py` |
| 경계 수렴 테스트 | `tests/test_boundary_convergence.py` |
| 통합 테스트 | `tests/test_integration.py` |
| 전체 테스트 실행 | `tests/run_all_tests.py` |

### 패키징

| 파일 | 경로 |
|------|------|
| 패키지 설정 | `setup.py` |
| 의존성 | `requirements.txt` |
| 라이선스 | `LICENSE` |
| Git 무시 | `.gitignore` |

---

## 🚀 빠른 접근

### 절대 경로

```bash
# 프로젝트 루트
cd /Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines/ThreeBodyBoundaryEngine

# 소스 코드
cd src/three_body_boundary_engine/

# 예제 실행
python3 examples/basic_usage.py

# 테스트 실행
python3 tests/test_three_body_boundary_engine.py
```

### Python에서 import

```python
# 프로젝트 루트를 경로에 추가
import sys
from pathlib import Path
project_root = Path("/Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines/ThreeBodyBoundaryEngine")
sys.path.insert(0, str(project_root / "src"))

# 엔진 import
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodyConfig,
    ThreeBodySystem,
    Body,
    Point
)
```

---

## 📊 파일 개수 요약

- **소스 파일**: 8개
- **테스트 파일**: 5개
- **예제 파일**: 1개
- **문서 파일**: 3개 (README, PHAM, 이 파일)
- **패키징 파일**: 4개 (setup.py, requirements.txt, LICENSE, .gitignore)

**총**: 21개 파일

---

## 🔍 파일 찾기 명령어

### 모든 Python 파일 찾기
```bash
find . -name "*.py" -type f
```

### 모든 문서 파일 찾기
```bash
find . -name "*.md" -type f
```

### 특정 파일 찾기
```bash
find . -name "three_body_boundary_engine.py"
```

---

**작성자**: GNJz (Qquarts)  
**버전**: 1.0.0

