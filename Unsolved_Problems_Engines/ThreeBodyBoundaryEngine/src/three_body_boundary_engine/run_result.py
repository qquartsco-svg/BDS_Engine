"""
ThreeBodyBoundaryEngine - 표준 실행 결과 모델 (L0/L1/L2 통합 반환)

외부 사용자는 엔진을 "하나의 엔트리포인트"로 사용하되,
내부 레이어(L0/L1/L2)는 모듈로 분리 유지한다.

Author: GNJz (Qquarts)
Version: 1.2.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .models import StabilityAnalysis, ThreeBodySystem
from .failure_atlas import FailureAtlas, FailureRecord
from .failure_bias_converter import SearchBias


@dataclass(frozen=True)
class EngineRunResult:
    """통합 실행 결과

    - analysis: L0 출력 (항상 존재)
    - failure_atlas: L1 누적 결과 (enable_l1 또는 입력 제공 시)
    - search_bias: L2 출력 (enable_l2 시)
    - last_failure_record: 이번 실행에서 추가로 기록된 실패 (실패가 아닐 경우 None)
    - system: 분석한 시스템 (추적용; 상태 변형 없음)
    """

    system: ThreeBodySystem
    analysis: StabilityAnalysis
    failure_atlas: Optional[FailureAtlas] = None
    search_bias: Optional[SearchBias] = None
    last_failure_record: Optional[FailureRecord] = None


