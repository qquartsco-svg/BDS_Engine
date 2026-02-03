"""
ThreeBodyBoundaryEngine - Failure Bias Converter 테스트

L2 레이어 (실패 학습 레이어) 테스트

Author: GNJz (Qquarts)
Version: 1.1.0
"""

import unittest
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from three_body_boundary_engine import (
    ThreeBodyBoundaryEngine,
    ThreeBodySystem,
    Body,
    Point,
    FailureAtlas,
    FailureBiasConverter,
    SearchBias
)


class TestFailureBiasConverter(unittest.TestCase):
    """Failure Bias Converter 테스트"""
    
    def setUp(self):
        """테스트 설정"""
        self.engine = ThreeBodyBoundaryEngine()
        self.atlas = FailureAtlas()
        self.converter = FailureBiasConverter(
            risk_decay_factor=0.9,
            min_risk_threshold=0.1
        )
        
        # 테스트용 삼체 시스템
        self.system = ThreeBodySystem(
            body1=Body(position=Point(0.0, 0.0), mass=1.0),
            body2=Body(position=Point(1.0, 0.0), mass=1.0),
            body3=Body(position=Point(0.5, 0.866), mass=1.0)
        )
    
    def test_bias_creation(self):
        """편향 생성 테스트"""
        # 실패 기록 생성
        analysis = self.engine.analyze_orbit_stability(self.system)
        self.atlas.record_failure(
            analysis=analysis,
            system=self.system,
            threshold=0.01
        )
        
        # 편향 생성
        bias = self.converter.convert_failure_to_bias(self.atlas)
        
        # 검증
        self.assertIsInstance(bias, SearchBias)
        self.assertIsInstance(bias.risk_map, dict)
        self.assertIsInstance(bias.collapse_mode_risk, dict)
        print(f"✅ 편향 생성: 총 위험도 {bias.total_risk_score:.3f}")
    
    def test_risk_map(self):
        """위험 지도 테스트"""
        # 여러 실패 기록 생성
        for i in range(3):
            analysis = self.engine.analyze_orbit_stability(self.system)
            self.atlas.record_failure(
                analysis=analysis,
                system=self.system,
                threshold=0.01
            )
        
        # 편향 생성
        bias = self.converter.convert_failure_to_bias(self.atlas)
        
        # 위험 지도 검증
        self.assertGreater(len(bias.risk_map), 0)
        print(f"✅ 위험 지도: {len(bias.risk_map)}개 조건")
    
    def test_should_avoid_condition(self):
        """조건 회피 판정 테스트"""
        # 실패 기록 생성
        analysis = self.engine.analyze_orbit_stability(self.system)
        record = self.atlas.record_failure(
            analysis=analysis,
            system=self.system,
            threshold=0.01
        )
        
        if record:
            # 편향 생성
            bias = self.converter.convert_failure_to_bias(self.atlas)
            
            # 회피 판정
            should_avoid = self.converter.should_avoid_condition(
                bias=bias,
                condition_signature=record.condition_signature,
                threshold=0.3
            )
            
            print(f"✅ 회피 판정: {should_avoid}")
            self.assertIsInstance(should_avoid, bool)
    
    def test_get_safe_conditions(self):
        """안전한 조건 필터링 테스트"""
        # 여러 실패 기록 생성
        for i in range(3):
            analysis = self.engine.analyze_orbit_stability(self.system)
            self.atlas.record_failure(
                analysis=analysis,
                system=self.system,
                threshold=0.01
            )
        
        # 편향 생성
        bias = self.converter.convert_failure_to_bias(self.atlas)
        
        # 후보 조건
        candidate_conditions = [
            record.condition_signature
            for record in self.atlas.failure_records[:3]
        ]
        
        # 안전한 조건 필터링
        safe_conditions = self.converter.get_safe_conditions(
            bias=bias,
            candidate_conditions=candidate_conditions,
            threshold=0.3
        )
        
        print(f"✅ 안전한 조건: {len(safe_conditions)}개")
        self.assertIsInstance(safe_conditions, list)
    
    def test_update_bias_with_new_failure(self):
        """새로운 실패 기록으로 편향 업데이트 테스트"""
        # 초기 실패 기록
        analysis = self.engine.analyze_orbit_stability(self.system)
        record = self.atlas.record_failure(
            analysis=analysis,
            system=self.system,
            threshold=0.01
        )
        
        if record:
            # 초기 편향 생성
            bias = self.converter.convert_failure_to_bias(self.atlas)
            initial_risk = bias.total_risk_score
            
            # 새로운 실패 기록으로 업데이트
            updated_bias = self.converter.update_bias_with_new_failure(
                bias=bias,
                new_record=record
            )
            
            # 검증
            self.assertIsInstance(updated_bias, SearchBias)
            print(f"✅ 편향 업데이트: {initial_risk:.3f} → {updated_bias.total_risk_score:.3f}")


if __name__ == "__main__":
    unittest.main()

