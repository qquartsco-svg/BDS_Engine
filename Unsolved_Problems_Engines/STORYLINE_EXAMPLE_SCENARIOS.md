# Storyline Layer Example Scenarios

**작성일**: 2026-02-05  
**상태**: 초안 (시나리오 예시용)

---

## 1️⃣ 목적

이 문서는 `Storyline Layer & Causal History Architecture`에서 정의한  
L1–L2–L3 구조가 **실제로 어떻게 쓰일 수 있는지**를  
두 가지 예시 시나리오로 보여주는 것을 목표로 한다.

- **시나리오 A**: 삼체 계열 시스템에서 “현재 상태 → 혼돈의 시작점” 재구성  
- **시나리오 B**: 가상의 사회/시스템 장애에서 “로그 붕괴 → 원인 스토리라인 복원”

각 시나리오는 **구체적인 데이터 흐름**에만 집중하며,  
실제 인물/사건 이름은 사용하지 않는다.

---

## 2️⃣ 시나리오 A – 삼체 계열 혼돈의 역사 재구성

### A-1. 상황 설정

- 다수의 삼체 시뮬레이션/운용 로그가 존재한다.
- 각 로그는 다음과 같은 정보를 포함한다:
  - 초기 조건 서명: `condition_signature`
  - 시뮬레이션 시간 또는 스텝: `t`
  - 위험도: `risk` (0.0 ~ 1.0)
  - 이벤트 타입: `event_type` (예: `NEAR_COLLAPSE`, `CAPTURE`, `ESCAPE`, `STABLE`)
- 현재 우리는 “심각한 혼돈 상태(예: CollapseZone 근처)”에 와 있는 한 궤도를 보고 있다.

질문:

> “이 궤도가 **어떤 조건과 사건들의 누적**을 통해  
>  지금의 혼돈 상태에 이르렀는가?”

### A-2. 데이터 변환 (L1 → L2)

1. UP-1 / StateManifold에서 제공하는 로그를 `DataFragment`로 변환:

```python
from historical_data_reconstructor import DataFragment

def log_to_fragment(log) -> DataFragment:
    content = f"cond={log.condition_signature}, event={log.event_type}, risk={log.risk:.2f}"
    source = "ThreeBodyBoundaryEngine"
    timestamp = log.time  # 또는 step 인덱스를 시간축으로 사용
    return DataFragment(content=content, source=source, timestamp=timestamp)
```

2. 현재 관측 중인 궤도 상태도 하나의 `DataFragment`로 표현:

```python
current_fragment = DataFragment(
    content="current_orbit_state, near_collapse=True",
    source="StateManifoldEngine",
    timestamp=current_time
)
```

### A-3. 스토리라인 재구성 (L2)

1. 모든 과거 로그 + 현재 상태를 `HistoricalDataReconstructor`에 전달:

```python
from historical_data_reconstructor import HistoricalDataReconstructor

reconstructor = HistoricalDataReconstructor(
    observer_id="three_body_analyzer",
    similarity_threshold=0.3
)

scattered_data = [
    {
        "content": frag.content,
        "source": frag.source,
        "timestamp": frag.timestamp,
    }
    for frag in past_fragments + [current_fragment]
]

chain = reconstructor.reconstruct_from_scattered_data(scattered_data)
origin = reconstructor.trace_back_to_origin(chain)
```

2. 결과 해석:
   - `chain.fragments`:
     - 초기 조건 → 중간 이벤트들 → 현재 혼돈 상태로 이어지는 **스토리라인**.
   - `origin`:
     - “처음으로 위험도가 의미 있게 증가하기 시작한 상태”  
       또는 “궤도의 운명이 바뀌기 시작한 전환점”에 해당.

### A-4. 투명한 기록으로 고정 (L3, 선택적)

원한다면, 이 분석 결과를 `TransparencyEngine`에 `LOCKED` 로 기록:

```python
from transparency_engine import TransparencyEngine, DecisionContext, RecordStage

engine = TransparencyEngine(...)

for i, fragment in enumerate(chain.fragments):
    context = DecisionContext(
        input_info_hash=fragment.context_hash,
        reference_docs=[fragment.source],
        external_conditions={
            "timestamp": fragment.timestamp,
            "story_position": i,
        },
        decision_rationale="three-body chaos storyline reconstruction"
    )
    engine.record_decision(
        decision_type="three_body_storyline",
        context=context,
        stage=RecordStage.LOCKED
    )
```

이로써:

- 삼체 계열 시스템에서 **“현재 상태 → 혼돈의 시작점”** 으로 이어지는  
  인과적 역사가 하나의 체인으로 남는다.

---

## 3️⃣ 시나리오 B – 가상의 사회/시스템 장애 히스토리 복원

### B-1. 상황 설정

- 가상의 국가/기업 시스템에서 **대규모 서비스 장애**가 발생했다.
- 장애 후:
  - 일부 로그는 남아 있고,
  - 일부는 누락·손상·삭제되어 있다.
- 다양한 출처:
  - 시스템 로그, 애플리케이션 로그
  - 운영자 채팅/이메일 요약
  - 공지/보도자료 초안

질문:

> “이 장애는 **어떤 사건 시퀀스**를 통해 발생했는가?  
>  그리고 **어느 시점에서 다른 선택을 했으면 피할 수 있었는가?**”

### B-2. 데이터 변환 (L1 → L2)

L1은 여기서 “사회적/기술적 센서층”으로 일반화된다:

- 각 로그/기록을 `DataFragment`로 변환:

```python
DataFragment(
    content="ERROR 500 at /api/v1/checkout",
    source="app_server_01",
    timestamp=...,
)

DataFragment(
    content="운영자 A: 배포 롤백 필요할지도?",
    source="chat_ops_room",
    timestamp=...,
)

DataFragment(
    content="공식 공지 초안 v1 - 장애 원인: 네트워크 불안정",
    source="internal_wiki",
    timestamp=...,
)
```

### B-3. 스토리라인 재구성 (L2)

1. `HistoricalDataReconstructor` 에 모든 조각을 투입:

```python
reconstructor = HistoricalDataReconstructor(
    observer_id="incident_review_board",
    similarity_threshold=0.25
)

scattered_data = [... DataFragment 기반 딕셔너리 ...]
chain = reconstructor.reconstruct_from_scattered_data(scattered_data)
origin = reconstructor.trace_back_to_origin(chain)
```

2. 결과:
   - `chain.fragments`:
     - 사전 징후 → 경고 무시/오판 → 첫 장애 → 확산 → 대응 실패 → 최종 다운  
       으로 이어지는 **장애 스토리라인**.
   - `origin`:
     - “처음으로 위험 신호가 명확하게 등장한 지점”  
       혹은 “다른 선택이 가능했던 분기점” 으로 해석 가능.

### B-4. 투명성 확보 (L3)

1. 이 스토리라인을 `TransparencyEngine` 에 `SEALED` 또는 `LOCKED` 로 기록하면:
   - 나중에 “장애 원인 조작”, “희생양 만들기” 등을 막을 수 있다.
2. 동시에:
   - `SEALED` 단계와 `AppealChain` 을 활용하면  
     “이 해석에 대한 이의 제기/보완” 을 **새로운 레이어**로 쌓아 나갈 수 있다.

---

## 4️⃣ 마무리 – 공통 패턴

두 시나리오 모두 다음과 같은 공통 패턴을 가진다:

1. **센서/지형 층 (L1)**  
   - 물리/사회 시스템에서 나온 **원시 로그**를 그대로 축적한다.
2. **스토리라인/히스토리 층 (L2)**  
   - 이 조각들을 `P(x, t)` 형태의 `DataFragment` 로 통일  
   - 문맥 유사도 + 인과 규칙으로 **인과적 역사(스토리라인)** 를 재구성  
   - 현재 상태에서 **혼돈/장애의 시작점**으로 이어지는 경로를 찾는다.
3. **앵커/투명성 층 (L3)**  
   - 이 재구성 결과를 **되돌릴 수 없는 기록**으로 고정하여  
     이후의 역사 조작/책임 회피를 구조적으로 어렵게 만든다.

이 문서는, 실제 구현된 엔진들을  
현실 문제(물리적 혼돈, 사회적 장애, 기록 붕괴)에  
어떻게 적용할 수 있는지에 대한 **첫 번째 시나리오 모음집**이다.

향후에는:
- 더 구체적인 수치 예시,
- 실제 또는 공개된 익명 데이터셋을 활용한 데모 코드,
- 시각화 예시(타임라인/그래프 등)를 추가할 수 있다.

---

**작성자**: GNJz (Qquarts)  
**버전**: 0.1.0  
**날짜**: 2026-02-05


