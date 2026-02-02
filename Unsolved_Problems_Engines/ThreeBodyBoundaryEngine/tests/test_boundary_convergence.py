"""
Boundary Convergence Adapter - 테스트

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import sys
from pathlib import Path
import math

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from three_body_boundary_engine.boundary_convergence_adapter import BoundaryConvergenceAdapter
from three_body_boundary_engine.point import Point


def test_boundary_convergence():
    """경계 수렴 어댑터 테스트"""
    print("\n" + "=" * 60)
    print("Boundary Convergence Adapter 테스트")
    print("=" * 60)
    
    adapter = BoundaryConvergenceAdapter(
        boundary_radius=1.0,
        initial_boundary_points=20,
        max_iterations=100,
        error_threshold=1e-6
    )
    
    # 초기 경계 생성
    boundary = adapter.generate_initial_boundary(20)
    assert len(boundary) == 20
    print(f"✅ 초기 경계 생성: {len(boundary)}개 점")
    
    # 둘레 계산
    perimeter = adapter.calculate_perimeter(boundary)
    theoretical_perimeter = 2 * math.pi * 1.0
    print(f"✅ 둘레 계산: {perimeter:.6f} (이론값: {theoretical_perimeter:.6f})")
    
    # 면적 계산
    area = adapter.calculate_area(boundary)
    theoretical_area = math.pi * 1.0 * 1.0
    print(f"✅ 면적 계산: {area:.6f} (이론값: {theoretical_area:.6f})")
    
    # 불일치 계산
    mismatch = adapter.calculate_mismatch(
        perimeter=perimeter,
        area=area,
        radius=1.0
    )
    assert mismatch >= 0.0
    print(f"✅ 불일치 계산: {mismatch:.6f}")
    
    # 수렴 실행 (밀도 없이)
    result = adapter.converge(importance_weights=None)
    
    assert result is not None
    assert hasattr(result, 'converged')
    assert hasattr(result, 'mismatch')
    assert hasattr(result, 'iteration')
    assert hasattr(result, 'boundary_points')
    
    print(f"✅ 수렴 실행:")
    print(f"   - 수렴 여부: {result.converged}")
    print(f"   - 불일치: {result.mismatch:.6f}")
    print(f"   - 반복 횟수: {result.iteration}")
    print(f"   - 경계 점 개수: {result.boundary_points}")
    
    print("=" * 60)
    print("✅ Boundary Convergence Adapter 테스트 통과")
    print("=" * 60)


if __name__ == "__main__":
    test_boundary_convergence()

