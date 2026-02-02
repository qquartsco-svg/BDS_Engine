"""
ThreeBodyBoundaryEngine Configuration

엔진 번호: UP-1
역할: 삼체 문제 경계 정합 분석 설정

Author: GNJz (Qquarts)
Version: 1.1.0
"""

from dataclasses import dataclass


@dataclass
class ThreeBodyConfig:
    """ThreeBodyBoundaryEngine 설정"""
    
    # 중력 퍼텐셜 계산 파라미터
    gravitational_constant: float = 1.0  # G (정규화)
    potential_resolution: int = 100  # 퍼텐셜 계산 해상도
    
    # 밀도 변환 파라미터
    density_normalization: str = "max"  # "max" or "sum"
    
    # 경계 정합 분석 파라미터
    stability_threshold: float = 0.1  # 안정성 판정 임계값
    collapse_threshold: float = 1.0  # 붕괴 판정 임계값
    
    # Boundary Convergence Engine 설정 (독립 모듈이므로 직접 구현)
    boundary_radius: float = 1.0
    initial_boundary_points: int = 20
    max_iterations: int = 1000
    error_threshold: float = 1e-6
    
    # 라그랑주 점 분석 파라미터
    lagrange_analysis_enabled: bool = True
    lagrange_stability_threshold: float = 0.05
    
    def __post_init__(self):
        """설정 검증"""
        if self.gravitational_constant <= 0:
            raise ValueError("중력 상수는 양수여야 합니다")
        if self.stability_threshold <= 0:
            raise ValueError("안정성 임계값은 양수여야 합니다")
        if self.boundary_radius <= 0:
            raise ValueError("경계 반지름은 양수여야 합니다")

