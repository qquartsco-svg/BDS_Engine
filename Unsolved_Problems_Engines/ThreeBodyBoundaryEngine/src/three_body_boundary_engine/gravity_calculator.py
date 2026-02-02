"""
Gravity Calculator - 중력 퍼텐셜 계산

엔진 번호: UP-1
역할: 중력 퍼텐셜 계산 및 밀도 변환

수식:
V(x,y) = -G * Σ(m_i / r_i)
ρ(x,y) = V(x,y) / V_max  (정규화)

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import math
from typing import Dict, List
from .point import Point
from .models import Body


class GravityCalculator:
    """중력 퍼텐셜 계산기"""
    
    def __init__(self, gravitational_constant: float = 1.0):
        """
        Args:
            gravitational_constant: 중력 상수 G
        """
        self.G = gravitational_constant
    
    def calculate_potential(self, point: Point, bodies: List[Body]) -> float:
        """특정 점에서의 중력 퍼텐셜 계산
        
        수식: V(x,y) = -G * Σ(m_i / r_i)
        
        Args:
            point: 계산할 점
            bodies: 천체 리스트
        
        Returns:
            중력 퍼텐셜 값
        """
        potential = 0.0
        for body in bodies:
            distance = point.distance_to(body.position)
            if distance > 0:
                potential += body.mass / distance
        return -self.G * potential
    
    def create_potential_field(
        self,
        bodies: List[Body],
        x_range: tuple,
        y_range: tuple,
        resolution: int = 100
    ) -> Dict[Point, float]:
        """중력 퍼텐셜 필드 생성
        
        Args:
            bodies: 천체 리스트
            x_range: x 범위 (min, max)
            y_range: y 범위 (min, max)
            resolution: 해상도
        
        Returns:
            {Point: potential_value} 딕셔너리
        """
        potential_field = {}
        x_min, x_max = x_range
        y_min, y_max = y_range
        
        x_step = (x_max - x_min) / resolution
        y_step = (y_max - y_min) / resolution
        
        for i in range(resolution + 1):
            for j in range(resolution + 1):
                x = x_min + i * x_step
                y = y_min + j * y_step
                point = Point(x, y)
                potential = self.calculate_potential(point, bodies)
                potential_field[point] = potential
        
        return potential_field
    
    def potential_to_density(
        self,
        potential_field: Dict[Point, float],
        normalization: str = "max"
    ) -> Dict[Point, float]:
        """중력 퍼텐셜을 밀도로 변환
        
        수식: ρ(x,y) = V(x,y) / V_max  (정규화)
        
        Args:
            potential_field: 중력 퍼텐셜 필드
            normalization: 정규화 방법 ("max" or "sum")
        
        Returns:
            {Point: density_value} 딕셔너리
        """
        if not potential_field:
            return {}
        
        values = list(potential_field.values())
        
        if normalization == "max":
            # 최대값으로 정규화
            max_potential = max(values)
            min_potential = min(values)
            if max_potential == min_potential:
                # 모든 값이 같으면 균등 분포
                return {point: 0.5 for point in potential_field.keys()}
            
            # 0~1 범위로 정규화
            density_field = {}
            for point, potential in potential_field.items():
                normalized = (potential - min_potential) / (max_potential - min_potential)
                density_field[point] = normalized
        
        elif normalization == "sum":
            # 합으로 정규화
            sum_potential = sum(abs(v) for v in values)
            if sum_potential == 0:
                return {point: 0.0 for point in potential_field.keys()}
            
            density_field = {}
            for point, potential in potential_field.items():
                density_field[point] = abs(potential) / sum_potential
        
        else:
            raise ValueError(f"알 수 없는 정규화 방법: {normalization}")
        
        return density_field

