"""
Gravity Calculator - 테스트

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import sys
from pathlib import Path
import math

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from three_body_boundary_engine import (
    GravityCalculator,
    Body,
    Point
)


def test_gravity_calculator():
    """중력 계산기 테스트"""
    print("\n" + "=" * 60)
    print("Gravity Calculator 테스트")
    print("=" * 60)
    
    calculator = GravityCalculator(gravitational_constant=1.0)
    
    # 단일 천체
    body = Body(position=Point(0.0, 0.0), mass=1.0)
    test_point = Point(1.0, 0.0)
    
    potential = calculator.calculate_potential(test_point, [body])
    
    # 거리 1, 질량 1이면 퍼텐셜 = -G * (1/1) = -1
    expected = -1.0
    assert abs(potential - expected) < 1e-6, f"퍼텐셜 계산 오류: {potential} != {expected}"
    print(f"✅ 단일 천체 퍼텐셜 계산: {potential:.6f}")
    
    # 다중 천체
    bodies = [
        Body(position=Point(0.0, 0.0), mass=1.0),
        Body(position=Point(1.0, 0.0), mass=1.0)
    ]
    test_point = Point(0.5, 0.0)
    
    potential = calculator.calculate_potential(test_point, bodies)
    print(f"✅ 다중 천체 퍼텐셜 계산: {potential:.6f}")
    
    # 퍼텐셜 필드 생성
    potential_field = calculator.create_potential_field(
        bodies=bodies,
        x_range=(-1.0, 2.0),
        y_range=(-1.0, 1.0),
        resolution=10
    )
    
    assert len(potential_field) > 0
    print(f"✅ 퍼텐셜 필드 생성: {len(potential_field)}개 점")
    
    # 밀도 변환
    density_field = calculator.potential_to_density(
        potential_field=potential_field,
        normalization="max"
    )
    
    assert len(density_field) == len(potential_field)
    
    # 밀도 값 범위 검증 (0~1)
    for density in density_field.values():
        assert 0.0 <= density <= 1.0
    
    print(f"✅ 밀도 변환: {len(density_field)}개 점, 범위 [0, 1]")
    
    print("=" * 60)
    print("✅ Gravity Calculator 테스트 통과")
    print("=" * 60)


if __name__ == "__main__":
    test_gravity_calculator()

