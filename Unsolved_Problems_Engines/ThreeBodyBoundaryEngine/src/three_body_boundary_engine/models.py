"""
ThreeBodyBoundaryEngine - 데이터 모델

엔진 번호: UP-1
역할: 삼체 문제 경계 정합 분석을 위한 데이터 구조

Author: GNJz (Qquarts)
Version: 1.2.0
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from .point import Point


@dataclass
class Body:
    """천체 정보"""
    position: Point
    mass: float
    velocity: Optional[Point] = None
    
    def __post_init__(self):
        """검증"""
        if self.mass <= 0:
            raise ValueError("질량은 양수여야 합니다")


@dataclass
class ThreeBodySystem:
    """삼체 시스템"""
    body1: Body
    body2: Body
    body3: Body
    gravitational_constant: float = 1.0  # G (정규화)
    
    def get_all_bodies(self) -> List[Body]:
        """모든 천체 반환"""
        return [self.body1, self.body2, self.body3]


@dataclass
class StabilityAnalysis:
    """안정성 분석 결과"""
    converged: bool
    mismatch: float
    iteration: int
    boundary_points: int
    stability_score: float  # 0.0 (불안정) ~ 1.0 (안정)
    convergence_rate: float
    
    def is_stable(self, threshold: float = 0.1) -> bool:
        """안정 여부 판정"""
        return self.mismatch < threshold and self.converged


@dataclass
class BoundaryDynamics:
    """경계 동역학 관찰 결과"""
    time_steps: List[float]
    mismatches: List[float]
    boundary_evolutions: List[int]  # 경계 점 개수 변화
    stability_trajectory: List[float]  # 안정성 점수 변화
    
    def get_collapse_point(self, threshold: float = 1.0) -> Optional[float]:
        """붕괴 시점 반환 (mismatch > threshold)"""
        for i, mismatch in enumerate(self.mismatches):
            if mismatch > threshold:
                return self.time_steps[i]
        return None


@dataclass
class LagrangePoint:
    """라그랑주 점"""
    position: Point
    lagrange_type: str  # "L1", "L2", "L3", "L4", "L5"
    stability: str  # "stable" or "unstable"


@dataclass
class LagrangeAnalysis:
    """라그랑주 점 분석 결과"""
    lagrange_points: List[LagrangePoint]
    stability_map: Dict[str, float]  # 각 라그랑주 점의 안정성 점수
    boundary_formation: Dict[str, StabilityAnalysis]  # 각 라그랑주 점의 경계 형성 분석



