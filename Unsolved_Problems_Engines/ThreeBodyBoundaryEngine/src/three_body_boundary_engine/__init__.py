"""
ThreeBodyBoundaryEngine - 삼체 문제 경계 정합 분석 엔진

엔진 번호: UP-1 (Unsolved Problems Engine #1)
엔진 이름: ThreeBodyBoundaryEngine
역할: 삼체 궤도 정합 분석을 통한 원인 구조 분석

⚠️ 중요 명확화:
- 이 엔진은 삼체 문제의 "해"를 제공하는 것이 아니라,
- 경계 정합 관점에서 궤도 안정성을 분석합니다.
- 출력은 "정답"이 아니라 "원인 분석 데이터"입니다.

핵심 철학:
- 안정 궤도 = 경계-공간 정합 상태
- 혼돈 = 경계 refinement 실패
- "왜 특정 지점에서 궤도가 붕괴하는가" 원인 분석

Author: GNJz (Qquarts)
Version: 1.0.0
"""

from .three_body_boundary_engine import ThreeBodyBoundaryEngine
from .config import ThreeBodyConfig
from .models import (
    Body,
    ThreeBodySystem,
    StabilityAnalysis,
    BoundaryDynamics,
    LagrangeAnalysis
)
from .point import Point

__version__ = "1.0.0"
__all__ = [
    "ThreeBodyBoundaryEngine",
    "ThreeBodyConfig",
    "Body",
    "Point",
    "ThreeBodySystem",
    "StabilityAnalysis",
    "BoundaryDynamics",
    "LagrangeAnalysis"
]

