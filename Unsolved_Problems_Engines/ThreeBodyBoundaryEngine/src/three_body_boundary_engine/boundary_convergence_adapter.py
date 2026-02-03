"""
Boundary Convergence Adapter - 경계 수렴 엔진 어댑터

엔진 번호: UP-1
역할: Boundary Convergence Engine을 독립적으로 사용하기 위한 어댑터

⚠️ 중요: 이 모듈은 Boundary Convergence Engine의 핵심 로직을
독립적으로 재구현하여 외부 의존성을 제거합니다.

Author: GNJz (Qquarts)
Version: 1.2.0
"""

import math
from typing import Dict, List, Optional
from .point import Point
from dataclasses import dataclass


@dataclass
class ConvergenceResult:
    """수렴 결과"""
    converged: bool
    mismatch: float
    iteration: int
    boundary_points: int
    perimeter_estimate: float
    area_estimate: float
    convergence_rate: float


class BoundaryConvergenceAdapter:
    """경계 수렴 어댑터 (독립 구현)"""
    
    def __init__(
        self,
        boundary_radius: float = 1.0,
        initial_boundary_points: int = 20,
        max_iterations: int = 1000,
        error_threshold: float = 1e-6
    ):
        """
        Args:
            boundary_radius: 경계 반지름
            initial_boundary_points: 초기 경계 점 개수
            max_iterations: 최대 반복 횟수
            error_threshold: 오차 임계값
        """
        self.boundary_radius = boundary_radius
        self.initial_boundary_points = initial_boundary_points
        self.max_iterations = max_iterations
        self.error_threshold = error_threshold
    
    def generate_initial_boundary(self, n_points: int) -> List[Point]:
        """초기 경계 생성 (원형 근사)
        
        수식: P_i = (r * cos(2πi/N), r * sin(2πi/N))
        """
        boundary = []
        for i in range(n_points):
            angle = 2 * math.pi * i / n_points
            x = self.boundary_radius * math.cos(angle)
            y = self.boundary_radius * math.sin(angle)
            boundary.append(Point(x, y))
        return boundary
    
    def calculate_perimeter(self, boundary: List[Point]) -> float:
        """경계 둘레 계산"""
        if len(boundary) < 2:
            return 0.0
        
        perimeter = 0.0
        for i in range(len(boundary)):
            next_i = (i + 1) % len(boundary)
            perimeter += boundary[i].distance_to(boundary[next_i])
        return perimeter
    
    def calculate_area(self, boundary: List[Point]) -> float:
        """면적 계산 (Shoelace 공식)
        
        수식: A = (1/2) * |Σ(x_i * y_{i+1} - x_{i+1} * y_i)|
        """
        if len(boundary) < 3:
            return 0.0
        
        area = 0.0
        for i in range(len(boundary)):
            next_i = (i + 1) % len(boundary)
            area += boundary[i].x * boundary[next_i].y
            area -= boundary[next_i].x * boundary[i].y
        return abs(area) / 2.0
    
    def calculate_mismatch(
        self,
        perimeter: float,
        area: float,
        radius: float
    ) -> float:
        """불일치 계산
        
        수식: Δ = (|P - 2πr| / 2πr + |A - πr²| / πr²) / 2
        """
        theoretical_perimeter = 2 * math.pi * radius
        theoretical_area = math.pi * radius * radius
        
        if theoretical_perimeter == 0 or theoretical_area == 0:
            return float('inf')
        
        perimeter_error = abs(perimeter - theoretical_perimeter) / theoretical_perimeter
        area_error = abs(area - theoretical_area) / theoretical_area
        
        return (perimeter_error + area_error) / 2.0
    
    def converge(
        self,
        importance_weights: Optional[Dict[Point, float]] = None
    ) -> ConvergenceResult:
        """경계 수렴 실행
        
        Args:
            importance_weights: 중요도 가중치 (밀도 분포)
        
        Returns:
            수렴 결과
        """
        # 초기 경계 생성
        boundary = self.generate_initial_boundary(self.initial_boundary_points)
        
        previous_mismatch = float('inf')
        iteration = 0
        
        while iteration < self.max_iterations:
            # 경계 길이 및 면적 계산
            perimeter = self.calculate_perimeter(boundary)
            area = self.calculate_area(boundary)
            
            # 불일치 계산
            mismatch = self.calculate_mismatch(
                perimeter=perimeter,
                area=area,
                radius=self.boundary_radius
            )
            
            # 수렴 확인
            if mismatch < self.error_threshold:
                return ConvergenceResult(
                    converged=True,
                    mismatch=mismatch,
                    iteration=iteration + 1,
                    boundary_points=len(boundary),
                    perimeter_estimate=perimeter,
                    area_estimate=area,
                    convergence_rate=abs(previous_mismatch - mismatch) if previous_mismatch != float('inf') else 0.0
                )
            
            # 수렴률 계산
            convergence_rate = abs(previous_mismatch - mismatch) if previous_mismatch != float('inf') else 0.0
            
            # 발산 확인
            if mismatch > previous_mismatch * 10:  # 급격한 발산
                return ConvergenceResult(
                    converged=False,
                    mismatch=mismatch,
                    iteration=iteration + 1,
                    boundary_points=len(boundary),
                    perimeter_estimate=perimeter,
                    area_estimate=area,
                    convergence_rate=convergence_rate
                )
            
            # 경계 정제 (간단한 재샘플링)
            if iteration % 3 == 0 and len(boundary) < 200:
                # 경계 점 개수 증가
                new_boundary = self.generate_initial_boundary(len(boundary) * 2)
                boundary = new_boundary
            
            previous_mismatch = mismatch
            iteration += 1
        
        # 최대 반복 횟수 도달
        return ConvergenceResult(
            converged=False,
            mismatch=mismatch,
            iteration=iteration,
            boundary_points=len(boundary),
            perimeter_estimate=perimeter,
            area_estimate=area,
            convergence_rate=convergence_rate if previous_mismatch != float('inf') else 0.0
        )

