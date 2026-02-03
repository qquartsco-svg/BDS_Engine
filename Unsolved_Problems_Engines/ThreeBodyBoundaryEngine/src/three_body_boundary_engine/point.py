"""
Point - 2D 점 모델

Author: GNJz (Qquarts)
Version: 1.2.0
"""

import math
from dataclasses import dataclass


@dataclass
class Point:
    """2D 점"""
    x: float
    y: float
    
    def distance_to(self, other: 'Point') -> float:
        """다른 점까지의 거리"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __hash__(self):
        """해시 가능하게"""
        return hash((round(self.x, 9), round(self.y, 9)))
    
    def __eq__(self, other) -> bool:
        """등호 비교 (부동소수점 오차 고려)"""
        if not isinstance(other, Point):
            return False
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9

