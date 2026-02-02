"""
Lagrange Calculator - 라그랑주 점 계산

엔진 번호: UP-1
역할: 라그랑주 점 계산 및 안정성 분석

라그랑주 점:
- L1, L2, L3: 불안정 (collinear)
- L4, L5: 안정 (equilateral triangle)

Author: GNJz (Qquarts)
Version: 1.1.0
"""

import math
from typing import List, Tuple
from .point import Point
from .models import Body, LagrangePoint


class LagrangeCalculator:
    """라그랑주 점 계산기"""
    
    def calculate_lagrange_points(
        self,
        body1: Body,
        body2: Body,
        body3: Body
    ) -> List[LagrangePoint]:
        """라그랑주 점 계산
        
        Args:
            body1, body2, body3: 삼체 시스템
        
        Returns:
            라그랑주 점 리스트
        """
        lagrange_points = []
        
        # 간단한 구현: 두 천체 간의 라그랑주 점 계산
        # 실제로는 세 천체 모두 고려해야 하지만, 여기서는 body1-body2 시스템 기준
        
        # L1, L2, L3 (collinear points)
        # 간단한 근사: 두 천체 사이의 중간점 근처
        mid_point = Point(
            (body1.position.x + body2.position.x) / 2,
            (body1.position.y + body2.position.y) / 2
        )
        
        distance = body1.position.distance_to(body2.position)
        if distance > 0:
            # L1 (body1과 body2 사이)
            l1 = Point(
                body1.position.x + (body2.position.x - body1.position.x) * 0.5,
                body1.position.y + (body2.position.y - body1.position.y) * 0.5
            )
            lagrange_points.append(LagrangePoint(
                position=l1,
                lagrange_type="L1",
                stability="unstable"
            ))
            
            # L2 (body2 너머)
            l2 = Point(
                body2.position.x + (body2.position.x - body1.position.x) * 0.1,
                body2.position.y + (body2.position.y - body1.position.y) * 0.1
            )
            lagrange_points.append(LagrangePoint(
                position=l2,
                lagrange_type="L2",
                stability="unstable"
            ))
            
            # L3 (body1 반대편)
            l3 = Point(
                body1.position.x - (body2.position.x - body1.position.x) * 0.1,
                body1.position.y - (body2.position.y - body1.position.y) * 0.1
            )
            lagrange_points.append(LagrangePoint(
                position=l3,
                lagrange_type="L3",
                stability="unstable"
            ))
            
            # L4, L5 (equilateral triangle points)
            # 정삼각형의 세 번째 꼭짓점
            dx = body2.position.x - body1.position.x
            dy = body2.position.y - body1.position.y
            
            # 60도 회전
            cos60 = 0.5
            sin60 = math.sqrt(3) / 2
            
            # L4
            l4_x = body1.position.x + dx * cos60 - dy * sin60
            l4_y = body1.position.y + dx * sin60 + dy * cos60
            lagrange_points.append(LagrangePoint(
                position=Point(l4_x, l4_y),
                lagrange_type="L4",
                stability="stable"
            ))
            
            # L5
            l5_x = body1.position.x + dx * cos60 + dy * sin60
            l5_y = body1.position.y - dx * sin60 + dy * cos60
            lagrange_points.append(LagrangePoint(
                position=Point(l5_x, l5_y),
                lagrange_type="L5",
                stability="stable"
            ))
        
        return lagrange_points

