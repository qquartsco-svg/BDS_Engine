# UP-2: Boundary Safe Search Engine (L3) 설계 문서

**엔진 번호**: UP-2 (Unsolved Problems Engine #2)  
**엔진 이름**: BoundarySafeSearchEngine  
**역할**: 위험 지형 위에서 안전한 경로 탐색  
**상태**: 설계 단계 (구현 대기)

---

## 🎯 핵심 정체성

### 우리가 하지 않는 것
- ❌ 강화학습 (Reinforcement Learning)
- ❌ 최적화 (Optimization)
- ❌ 정책 생성 (Policy Generation)
- ❌ "삼체 문제를 푼다"

### 우리가 하는 것
- ✅ Constraint-aware path selection
- ✅ Risk-weighted search
- ✅ 수렴 보장 우선 탐색
- ✅ "붕괴하지 않는 경로만 고른다"

---

## 📐 아키텍처 원칙

### UP-1과의 관계

**UP-1 (ThreeBodyBoundaryEngine)**:
- 입력: 삼체 시스템
- 출력: `EngineRunResult` (analysis, atlas, bias)
- 역할: 원인 분석 + 실패 지형 생성

**UP-2 (BoundarySafeSearchEngine)**:
- 입력: `SearchBias` (UP-1 L2 출력)
- 출력: `SafePath` (안전한 경로 후보)
- 역할: 위험 지형 위에서만 탐색

### 분리 원칙

```
UP-1 (완성, 봉인)          UP-2 (별도 엔진)
     │                           │
     └─── SearchBias ────────────┘
              │
              └─── SafePath
```

**중요**: UP-1 코드에 UP-2 로직이 들어가면 안 됨.

---

## 🔬 핵심 개념

### 1. 안전 영역 탐색

**기존 질문**: "해가 존재하는가?"

**우리의 질문**: "붕괴하지 않는 경로가 존재하는가?"

**핵심 아이디어**:
- 위험 지형 = L2가 만든 `SearchBias.risk_map`
- 안전 영역 = 위험도 < 임계값인 구간
- 경로 = 안전 영역만을 통과하는 경로

### 2. 수식

**위험도 기반 경로 점수**:
```
path_score = Σ(1 - risk_map[condition]) / path_length
```

**안전성 판정**:
```
safe_path: 모든 condition에서 risk < threshold
unsafe_path: 하나라도 risk >= threshold
```

**수렴 보장**:
```
convergence_guarantee = min(1 - risk) for all conditions in path
```

---

## 🏗️ 인터페이스 설계

### 클래스 구조

```python
class BoundarySafeSearch:
    """안전 영역 탐색 엔진"""
    
    def __init__(
        self,
        bias: SearchBias,
        risk_threshold: float = 0.5
    ):
        """
        Args:
            bias: UP-1 L2에서 생성된 탐색 편향
            risk_threshold: 위험도 임계값
        """
        pass
    
    def find_safe_path(
        self,
        start: ConditionSignature,
        goal: ConditionSignature,
        strategy: SearchStrategy = SearchStrategy.GREEDY
    ) -> Optional[SafePath]:
        """안전한 경로 탐색
        
        Args:
            start: 시작 조건 서명
            goal: 목표 조건 서명
            strategy: 탐색 전략 (GREEDY, A_STAR, PROBABILISTIC)
        
        Returns:
            안전한 경로 (없으면 None)
        """
        pass
    
    def evaluate_path_risk(
        self,
        path: List[ConditionSignature]
    ) -> float:
        """경로의 전체 위험도 평가"""
        pass


@dataclass
class SafePath:
    """안전한 경로"""
    path: List[ConditionSignature]  # 경로상의 조건 서명들
    total_risk: float  # 전체 위험도
    convergence_guarantee: float  # 수렴 보장도
    path_score: float  # 경로 점수


class SearchStrategy(Enum):
    """탐색 전략"""
    GREEDY = "greedy"  # 그리디 (가장 위험도 낮은 다음 노드)
    A_STAR = "a_star"  # A* (휴리스틱 + 위험도)
    PROBABILISTIC = "probabilistic"  # 확률적 (위험도 기반 샘플링)
```

---

## 🔄 데이터 흐름

```
UP-1.run() → EngineRunResult
    │
    └─── search_bias (L2 출력)
            │
            └─── UP-2.find_safe_path()
                    │
                    └─── SafePath
```

---

## ⚠️ 중요 제약 조건

### 1. 정체성 보호

- **"해결 엔진"이 아님**: 경로 후보만 제시
- **"최적화 엔진"이 아님**: 안전성만 보장
- **"정책 엔진"이 아님**: 행동 생성 안 함

### 2. UP-1과의 경계

- UP-1 코드 수정 ❌
- UP-1 의존성 추가 ❌
- UP-1 인터페이스 변경 ❌
- `SearchBias`만 입력으로 받음 ✅

### 3. 실험적 상태

- 물리적 검증 전까지 실험적
- 프로덕션 사용 금지
- 성능 측정 데이터 없음

---

## 📋 구현 체크리스트 (향후)

### Phase 1: 기본 탐색
- [ ] `BoundarySafeSearch` 클래스 구현
- [ ] `SafePath` 데이터 모델 구현
- [ ] 그리디 전략 구현
- [ ] 기본 테스트

### Phase 2: 고급 전략
- [ ] A* 전략 구현
- [ ] 확률적 전략 구현
- [ ] 경로 위험도 평가 구현

### Phase 3: 통합
- [ ] UP-1과의 통합 테스트
- [ ] 문서화
- [ ] PHAM 블록체인 서명

---

## 🎯 최종 목표

**UP-2는 UP-1의 "실패 지형" 위에서만 탐색하는 엔진이다.**

- 원인 분석 (UP-1) + 안전 탐색 (UP-2) = 완전한 분석 프레임워크
- 하지만 각각은 독립적으로 존재한다.
- UP-1은 이미 완성되었고, UP-2는 별도 프로젝트다.

---

**작성자**: GNJz (Qquarts)  
**작성일**: 2026-02-03  
**상태**: 설계 완료, 구현 대기

