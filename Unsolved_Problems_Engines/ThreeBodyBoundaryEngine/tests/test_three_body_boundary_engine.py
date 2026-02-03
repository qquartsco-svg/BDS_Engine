"""
ThreeBodyBoundaryEngine - 테스트

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import sys
import unittest
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodyConfig,
    ThreeBodySystem,
    Body,
    Point
)


class TestThreeBodyBoundaryEngine(unittest.TestCase):
    """ThreeBodyBoundaryEngine 테스트"""
    
    def test_engine_initialization(self):
        """엔진 초기화 테스트"""
        config = ThreeBodyConfig()
        engine = ThreeBodyBoundaryEngine(config)
        
        assert engine is not None
        assert engine.config is not None
        assert engine.gravity_calculator is not None
        assert engine.boundary_adapter is not None
        assert engine.lagrange_calculator is not None
    
    def test_orbit_stability_analysis(self):
        """궤도 안정성 분석 테스트"""
        config = ThreeBodyConfig()
        engine = ThreeBodyBoundaryEngine(config)
        
        # 정삼각형 배치 (상대적으로 안정)
        system = ThreeBodySystem(
            body1=Body(position=Point(0.0, 0.0), mass=1.0),
            body2=Body(position=Point(1.0, 0.0), mass=1.0),
            body3=Body(position=Point(0.5, 0.866), mass=1.0)
        )
        
        analysis = engine.analyze_orbit_stability(system)
        
        # 결과 검증
        assert analysis is not None
        assert hasattr(analysis, 'converged')
        assert hasattr(analysis, 'mismatch')
        assert hasattr(analysis, 'iteration')
        assert hasattr(analysis, 'boundary_points')
        assert hasattr(analysis, 'stability_score')
        assert hasattr(analysis, 'convergence_rate')
        
        # 안정성 점수 범위 검증
        assert 0.0 <= analysis.stability_score <= 1.0
        
        # 불일치는 0 이상
        assert analysis.mismatch >= 0.0
    
    def test_lagrange_points_observation(self):
        """라그랑주 점 경계 관찰 테스트"""
        config = ThreeBodyConfig()
        engine = ThreeBodyBoundaryEngine(config)
        
        system = ThreeBodySystem(
            body1=Body(position=Point(0.0, 0.0), mass=1.0),
            body2=Body(position=Point(1.0, 0.0), mass=1.0),
            body3=Body(position=Point(0.5, 0.866), mass=1.0)
        )
        
        lagrange_analysis = engine.observe_lagrange_points(system)
        
        # 결과 검증
        assert lagrange_analysis is not None
        assert hasattr(lagrange_analysis, 'lagrange_points')
        assert hasattr(lagrange_analysis, 'stability_map')
        assert hasattr(lagrange_analysis, 'boundary_formation')
        
        # 라그랑주 점 개수 검증 (L1~L5 = 5개)
        assert len(lagrange_analysis.lagrange_points) == 5
        
        # 각 라그랑주 점 타입 검증
        lagrange_types = [lp.lagrange_type for lp in lagrange_analysis.lagrange_points]
        assert "L1" in lagrange_types
        assert "L2" in lagrange_types
        assert "L3" in lagrange_types
        assert "L4" in lagrange_types
        assert "L5" in lagrange_types
    
    def test_stability_conditions_comparison(self):
        """안정/불안정 조건 비교 테스트"""
        config = ThreeBodyConfig()
        engine = ThreeBodyBoundaryEngine(config)
        
        # 다양한 초기 조건
        systems = [
            ThreeBodySystem(
                body1=Body(position=Point(0.0, 0.0), mass=1.0),
                body2=Body(position=Point(1.0, 0.0), mass=1.0),
                body3=Body(position=Point(0.5, 0.866), mass=1.0)
            ),  # 정삼각형
            ThreeBodySystem(
                body1=Body(position=Point(0.0, 0.0), mass=1.0),
                body2=Body(position=Point(2.0, 0.0), mass=1.0),
                body3=Body(position=Point(1.0, 1.0), mass=1.0)
            ),  # 더 멀리 떨어진 배치
        ]
        
        results = engine.compare_stability_conditions(systems)
        
        # 결과 검증
        assert len(results) == len(systems)
        
        for result in results:
            assert result is not None
            assert hasattr(result, 'stability_score')
            assert 0.0 <= result.stability_score <= 1.0
    
    def test_boundary_formation_observation(self):
        """경계 형성 과정 관찰 테스트"""
        config = ThreeBodyConfig()
        engine = ThreeBodyBoundaryEngine(config)
        
        system = ThreeBodySystem(
            body1=Body(position=Point(0.0, 0.0), mass=1.0),
            body2=Body(position=Point(1.0, 0.0), mass=1.0),
            body3=Body(position=Point(0.5, 0.866), mass=1.0)
        )
        
        time_steps = [0.0, 0.1, 0.2, 0.3]
        dynamics = engine.observe_boundary_formation(system, time_steps)
        
        # 결과 검증
        assert dynamics is not None
        assert hasattr(dynamics, 'time_steps')
        assert hasattr(dynamics, 'mismatches')
        assert hasattr(dynamics, 'boundary_evolutions')
        assert hasattr(dynamics, 'stability_trajectory')
        
        # 시간 단계 개수 검증
        assert len(dynamics.time_steps) == len(time_steps)
        assert len(dynamics.mismatches) == len(time_steps)
        assert len(dynamics.boundary_evolutions) == len(time_steps)
        assert len(dynamics.stability_trajectory) == len(time_steps)
    
    def test_causal_analysis_philosophy(self):
        """원인 분석 철학 검증 테스트"""
        config = ThreeBodyConfig()
        engine = ThreeBodyBoundaryEngine(config)
        
        system = ThreeBodySystem(
            body1=Body(position=Point(0.0, 0.0), mass=1.0),
            body2=Body(position=Point(1.0, 0.0), mass=1.0),
            body3=Body(position=Point(0.5, 0.866), mass=1.0)
        )
        
        analysis = engine.analyze_orbit_stability(system)
        
        # 원인 분석 철학 검증:
        # - 결과는 "정답"이 아니라 "원인 분석 데이터"
        # - 안정성 점수, 불일치 등은 관찰 가능한 데이터
        # - 이것으로부터 추론할 수 있음
        
        assert analysis.stability_score is not None  # 관찰 가능한 데이터
        assert analysis.mismatch is not None  # 관찰 가능한 데이터
        assert analysis.convergence_rate is not None  # 관찰 가능한 데이터
        
        # 이것이 "해"가 아니라 "원인 분석 데이터"임을 확인
        # (직접적인 검증은 어렵지만, 데이터 구조로 확인 가능)
        assert hasattr(analysis, 'is_stable')  # 추론 가능한 메서드


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("ThreeBodyBoundaryEngine - 테스트 실행")
    print("=" * 60)
    
    test_suite = TestThreeBodyBoundaryEngine()
    tests = [
        ("엔진 초기화", test_suite.test_engine_initialization),
        ("궤도 안정성 분석", test_suite.test_orbit_stability_analysis),
        ("라그랑주 점 경계 관찰", test_suite.test_lagrange_points_observation),
        ("안정/불안정 조건 비교", test_suite.test_stability_conditions_comparison),
        ("경계 형성 과정 관찰", test_suite.test_boundary_formation_observation),
        ("원인 분석 철학 검증", test_suite.test_causal_analysis_philosophy),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✅ {test_name}: 통과")
            passed += 1
        except Exception as e:
            print(f"❌ {test_name}: 실패 - {e}")
            failed += 1
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"테스트 결과: {passed}개 통과, {failed}개 실패")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

