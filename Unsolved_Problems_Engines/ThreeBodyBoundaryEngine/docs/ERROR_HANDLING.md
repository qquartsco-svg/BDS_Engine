# 에러 처리 가이드 - ThreeBodyBoundaryEngine

**엔진 번호**: UP-1  
**버전**: 1.2.0  
**최종 업데이트**: 2026-02-03

---

## 📚 목차

1. [일반적인 에러](#일반적인-에러)
2. [레이어별 에러 처리](#레이어별-에러-처리)
3. [에러 처리 베스트 프랙티스](#에러-처리-베스트-프랙티스)
4. [에러 복구 전략](#에러-복구-전략)

---

## 일반적인 에러

### `ValueError`

**발생 조건**:
- 질량이 0 이하인 경우
- 잘못된 범위 값
- 잘못된 임계값

**예제**:
```python
from three_body_boundary_engine import Body, Point

try:
    # 질량이 0 이하
    body = Body(position=Point(0, 0), mass=-1.0)
except ValueError as e:
    print(f"에러: {e}")
    # 출력: "질량은 양수여야 합니다"
```

**해결 방법**:
```python
# 올바른 사용
body = Body(position=Point(0, 0), mass=1.0)  # 양수 질량
```

---

### `TypeError`

**발생 조건**:
- 잘못된 타입의 매개변수 전달
- None 값이 필요한 곳에 다른 타입 전달

**예제**:
```python
from three_body_boundary_engine import ThreeBodyBoundaryEngine

engine = ThreeBodyBoundaryEngine()

try:
    # 잘못된 타입
    analysis = engine.analyze_orbit_stability("invalid")
except TypeError as e:
    print(f"에러: {e}")
```

**해결 방법**:
```python
from three_body_boundary_engine import ThreeBodySystem, Body, Point

# 올바른 타입 사용
system = ThreeBodySystem(
    body1=Body(position=Point(0, 0), mass=1.0),
    body2=Body(position=Point(1, 0), mass=1.0),
    body3=Body(position=Point(0.5, 0.866), mass=1.0)
)
analysis = engine.analyze_orbit_stability(system)
```

---

### `AttributeError`

**발생 조건**:
- 존재하지 않는 속성 접근
- None 객체의 속성 접근

**예제**:
```python
from three_body_boundary_engine import FailureAtlas

atlas = FailureAtlas()

try:
    # 빈 리스트에서 접근
    first_record = atlas.failure_records[0]
except (AttributeError, IndexError) as e:
    print(f"에러: {e}")
```

**해결 방법**:
```python
# 안전한 접근
if len(atlas.failure_records) > 0:
    first_record = atlas.failure_records[0]
else:
    print("실패 기록이 없습니다")
```

---

## 레이어별 에러 처리

### L0: 원인 분석 레이어

#### 입력 검증

```python
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodySystem,
    Body,
    Point
)

engine = ThreeBodyBoundaryEngine()

try:
    # 잘못된 시스템
    system = ThreeBodySystem(
        body1=Body(position=Point(0, 0), mass=-1.0),  # 잘못된 질량
        body2=Body(position=Point(1, 0), mass=1.0),
        body3=Body(position=Point(0.5, 0.866), mass=1.0)
    )
    analysis = engine.analyze_orbit_stability(system)
except ValueError as e:
    print(f"입력 검증 실패: {e}")
```

#### 범위 계산 실패

```python
try:
    # 범위가 너무 작은 경우
    analysis = engine.analyze_orbit_stability(
        system,
        x_range=(0, 0),  # 잘못된 범위
        y_range=(0, 0)
    )
except (ValueError, ZeroDivisionError) as e:
    print(f"범위 계산 실패: {e}")
    # 자동 계산 사용
    analysis = engine.analyze_orbit_stability(system)
```

---

### L1: 실패 추적 레이어

#### 빈 Atlas 처리

```python
from three_body_boundary_engine import FailureAtlas

atlas = FailureAtlas()

# 안전한 통계 확인
stats = atlas.get_failure_statistics()
if stats['total_failures'] == 0:
    print("실패 기록이 없습니다")
else:
    print(f"총 실패 횟수: {stats['total_failures']}")
```

#### 유사도 검색 실패

```python
from three_body_boundary_engine import FailureAtlas

atlas = FailureAtlas()

try:
    # 빈 Atlas에서 검색
    similar = atlas.get_similar_failures(
        condition_signature="test",
        similarity_threshold=0.5
    )
    # 빈 리스트 반환 (에러 아님)
    if len(similar) == 0:
        print("유사한 실패 패턴이 없습니다")
except Exception as e:
    print(f"검색 실패: {e}")
```

---

### L2: 실패 학습 레이어

#### 빈 Atlas로 편향 생성

```python
from three_body_boundary_engine import (
    FailureAtlas,
    FailureBiasConverter
)

atlas = FailureAtlas()
converter = FailureBiasConverter()

# 빈 Atlas로 편향 생성 (에러 아님)
bias = converter.convert_failure_to_bias(atlas)

# 빈 편향 확인
if bias.total_risk_score == 0.0:
    print("위험 지도가 비어 있습니다")
```

#### 잘못된 조건 서명

```python
from three_body_boundary_engine import FailureBiasConverter, SearchBias

converter = FailureBiasConverter()
bias = SearchBias()

try:
    # 잘못된 조건 서명
    should_avoid = converter.should_avoid_condition(
        bias=bias,
        condition_signature=None,  # None 값
        threshold=0.5
    )
except (TypeError, AttributeError) as e:
    print(f"에러: {e}")
```

---

## 에러 처리 베스트 프랙티스

### 1. 명시적 에러 처리

```python
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodySystem,
    Body,
    Point
)

engine = ThreeBodyBoundaryEngine()

def safe_analyze(system):
    """안전한 분석 함수"""
    try:
        analysis = engine.analyze_orbit_stability(system)
        return analysis
    except ValueError as e:
        print(f"입력 검증 실패: {e}")
        return None
    except Exception as e:
        print(f"예상치 못한 에러: {e}")
        return None

# 사용
system = ThreeBodySystem(...)
analysis = safe_analyze(system)
if analysis:
    print(f"안정성 점수: {analysis.stability_score}")
```

---

### 2. 기본값 사용

```python
from three_body_boundary_engine import FailureAtlas

atlas = FailureAtlas()

# 안전한 통계 확인
stats = atlas.get_failure_statistics()
total = stats.get('total_failures', 0)  # 기본값 0
print(f"총 실패 횟수: {total}")
```

---

### 3. 조건 확인 후 접근

```python
from three_body_boundary_engine import FailureAtlas

atlas = FailureAtlas()

# 조건 확인 후 접근
if len(atlas.failure_records) > 0:
    first_record = atlas.failure_records[0]
    print(f"첫 번째 실패: {first_record.collapse_mode.value}")
else:
    print("실패 기록이 없습니다")
```

---

### 4. 타입 검증

```python
from three_body_boundary_engine import (
    ThreeBodySystem,
    Body,
    Point
)

def create_system(body1, body2, body3):
    """안전한 시스템 생성"""
    if not all(isinstance(b, Body) for b in [body1, body2, body3]):
        raise TypeError("모든 인자는 Body 타입이어야 합니다")
    
    return ThreeBodySystem(
        body1=body1,
        body2=body2,
        body3=body3
    )

# 사용
try:
    system = create_system(body1, body2, body3)
except TypeError as e:
    print(f"타입 에러: {e}")
```

---

## 에러 복구 전략

### 1. 자동 재시도

```python
import time
from three_body_boundary_engine import ThreeBodyBoundaryEngine

def analyze_with_retry(engine, system, max_retries=3):
    """재시도 로직이 있는 분석"""
    for attempt in range(max_retries):
        try:
            analysis = engine.analyze_orbit_stability(system)
            return analysis
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"재시도 {attempt + 1}/{max_retries}: {e}")
                time.sleep(0.1)  # 짧은 대기
            else:
                raise
    
    return None
```

---

### 2. 폴백 전략

```python
from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodyConfig
)

def create_engine_with_fallback():
    """폴백이 있는 엔진 생성"""
    try:
        # 커스텀 설정 시도
        config = ThreeBodyConfig(
            boundary_radius=2.0,
            max_iterations=1000
        )
        return ThreeBodyBoundaryEngine(config)
    except Exception:
        # 기본 설정으로 폴백
        return ThreeBodyBoundaryEngine()
```

---

### 3. 로깅

```python
import logging
from three_body_boundary_engine import ThreeBodyBoundaryEngine

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = ThreeBodyBoundaryEngine()

try:
    analysis = engine.analyze_orbit_stability(system)
    logger.info(f"분석 성공: {analysis.stability_score}")
except Exception as e:
    logger.error(f"분석 실패: {e}", exc_info=True)
```

---

## 에러 코드 참조

### L0 에러

| 에러 | 원인 | 해결 방법 |
|------|------|----------|
| `ValueError: 질량은 양수여야 합니다` | 질량이 0 이하 | 양수 질량 사용 |
| `TypeError: ...` | 잘못된 타입 | 올바른 타입 사용 |
| `ZeroDivisionError` | 범위 계산 실패 | 자동 범위 계산 사용 |

### L1 에러

| 에러 | 원인 | 해결 방법 |
|------|------|----------|
| `IndexError` | 빈 리스트 접근 | 조건 확인 후 접근 |
| `AttributeError` | None 객체 접근 | None 체크 |

### L2 에러

| 에러 | 원인 | 해결 방법 |
|------|------|----------|
| `TypeError` | 잘못된 타입 | 타입 검증 |
| `AttributeError` | None 값 | 기본값 사용 |

---

## 추가 리소스

- [API Reference](./API_REFERENCE.md)
- [사용 가이드](./USAGE_GUIDE.md)

---

**작성자**: GNJz (Qquarts)  
**최종 업데이트**: 2026-02-03

