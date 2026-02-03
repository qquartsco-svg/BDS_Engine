#!/usr/bin/env python3
"""
ThreeBodyBoundaryEngine - 통합 테스트 실행 스크립트

터미널에서 실행하여 모든 테스트를 실행하고 상세한 결과를 출력합니다.

사용법:
    python3 run_tests.py
    또는
    chmod +x run_tests.py
    ./run_tests.py
"""

import sys
import time
from pathlib import Path
import unittest
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# 테스트 모듈 import
import tests.test_three_body_boundary_engine
import tests.test_failure_atlas
import tests.test_failure_bias_converter
import tests.test_integration
import tests.test_gravity_calculator
import tests.test_boundary_convergence

# 함수 기반 테스트를 unittest로 변환하기 위한 래퍼
import unittest
from unittest import TestCase

# 함수 기반 테스트를 TestCase로 변환
class IntegrationTestWrapper(TestCase):
    def test_causal_analysis_scenario(self):
        tests.test_integration.test_causal_analysis_scenario()
    
    def test_lagrange_stability_comparison(self):
        tests.test_integration.test_lagrange_stability_comparison()

class GravityCalculatorTestWrapper(TestCase):
    def test_gravity_calculator(self):
        tests.test_gravity_calculator.test_gravity_calculator()

class BoundaryConvergenceTestWrapper(TestCase):
    def test_boundary_convergence(self):
        tests.test_boundary_convergence.test_boundary_convergence()


def print_header(title):
    """헤더 출력"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_section(title):
    """섹션 출력"""
    print("\n" + "-" * 70)
    print(f"  {title}")
    print("-" * 70)


def run_all_tests():
    """모든 테스트 실행"""
    print_header("ThreeBodyBoundaryEngine 통합 테스트")
    print(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"버전: 1.2.0")
    
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 각 테스트 모듈 추가
    print_section("테스트 모듈 로드")
    
    # 클래스 기반 테스트
    modules = [
        ("L0: 원인 분석 레이어", tests.test_three_body_boundary_engine),
        ("L1: 실패 추적 레이어", tests.test_failure_atlas),
        ("L2: 실패 학습 레이어", tests.test_failure_bias_converter),
    ]
    
    for name, module in modules:
        tests_obj = loader.loadTestsFromModule(module)
        suite.addTests(tests_obj)
        print(f"  ✅ {name}: {tests_obj.countTestCases()}개 테스트 로드")
    
    # 함수 기반 테스트 (래퍼 사용)
    wrapper_modules = [
        ("통합 테스트", IntegrationTestWrapper),
        ("유닛 테스트 (중력 계산기)", GravityCalculatorTestWrapper),
        ("유닛 테스트 (경계 수렴)", BoundaryConvergenceTestWrapper),
    ]
    
    for name, wrapper_class in wrapper_modules:
        tests_obj = loader.loadTestsFromTestCase(wrapper_class)
        suite.addTests(tests_obj)
        print(f"  ✅ {name}: {tests_obj.countTestCases()}개 테스트 로드")
    
    print(f"\n총 테스트 수: {suite.countTestCases()}개")
    
    # 테스트 실행
    print_section("테스트 실행 시작")
    start_time = time.time()
    
    # 상세 출력을 위한 커스텀 스트림
    class DetailedTestResult(unittest.TextTestResult):
        def startTest(self, test):
            super().startTest(test)
            test_name = test._testMethodName
            class_name = test.__class__.__name__
            print(f"\n  [실행 중] {class_name}.{test_name}")
        
        def addSuccess(self, test):
            super().addSuccess(test)
            test_name = test._testMethodName
            class_name = test.__class__.__name__
            print(f"  ✅ 통과: {class_name}.{test_name}")
        
        def addFailure(self, test, err):
            super().addFailure(test, err)
            test_name = test._testMethodName
            class_name = test.__class__.__name__
            print(f"  ❌ 실패: {class_name}.{test_name}")
            print(f"     에러: {err[1]}")
        
        def addError(self, test, err):
            super().addError(test, err)
            test_name = test._testMethodName
            class_name = test.__class__.__name__
            print(f"  ⚠️ 에러: {class_name}.{test_name}")
            print(f"     에러: {err[1]}")
    
    # 커스텀 러너 생성
    class DetailedTestRunner(unittest.TextTestRunner):
        def __init__(self, *args, **kwargs):
            kwargs['resultclass'] = DetailedTestResult
            super().__init__(*args, **kwargs)
    
    runner = DetailedTestRunner(verbosity=0, stream=sys.stdout)
    result = runner.run(suite)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # 결과 요약
    print_header("테스트 결과 요약")
    
    print(f"\n📊 전체 통계:")
    print(f"  총 테스트 수: {result.testsRun}개")
    print(f"  성공: {result.testsRun - len(result.failures) - len(result.errors)}개 ✅")
    print(f"  실패: {len(result.failures)}개")
    print(f"  에러: {len(result.errors)}개")
    print(f"  성공률: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")
    print(f"  실행 시간: {elapsed_time:.3f}초")
    print(f"  평균 시간: {elapsed_time / result.testsRun * 1000:.3f}ms/테스트")
    
    # 레이어별 통계
    print_section("레이어별 테스트 결과")
    
    # 모듈별 테스트 수 계산
    l0_count = loader.loadTestsFromModule(tests.test_three_body_boundary_engine).countTestCases()
    l1_count = loader.loadTestsFromModule(tests.test_failure_atlas).countTestCases()
    l2_count = loader.loadTestsFromModule(tests.test_failure_bias_converter).countTestCases()
    integration_count = loader.loadTestsFromTestCase(IntegrationTestWrapper).countTestCases()
    unit_count = loader.loadTestsFromTestCase(GravityCalculatorTestWrapper).countTestCases() + loader.loadTestsFromTestCase(BoundaryConvergenceTestWrapper).countTestCases()
    
    print(f"  ✅ L0 (원인 분석): {l0_count}개 테스트")
    print(f"  ✅ L1 (실패 추적): {l1_count}개 테스트")
    print(f"  ✅ L2 (실패 학습): {l2_count}개 테스트")
    if integration_count > 0:
        print(f"  ✅ 통합 테스트: {integration_count}개 테스트")
    if unit_count > 0:
        print(f"  ✅ 유닛 테스트: {unit_count}개 테스트")
    
    # 실패한 테스트 상세
    if result.failures:
        print_section("실패한 테스트 상세")
        for test, traceback in result.failures:
            print(f"\n  ❌ {test}")
            print(f"     {traceback.split(chr(10))[-2]}")
    
    # 에러 발생 테스트 상세
    if result.errors:
        print_section("에러 발생 테스트 상세")
        for test, traceback in result.errors:
            print(f"\n  ⚠️ {test}")
            print(f"     {traceback.split(chr(10))[-2]}")
    
    # 최종 결론
    print_header("최종 결론")
    
    if result.wasSuccessful():
        print("\n✅ 모든 테스트가 성공적으로 통과했습니다!")
        print("\n📋 검증된 항목:")
        print("  ✅ L0: 원인 분석 레이어 정상 작동")
        print("  ✅ L1: 실패 추적 레이어 정상 작동")
        print("  ✅ L2: 실패 학습 레이어 정상 작동")
        print("  ✅ 통합 파이프라인 정상 작동")
        print("  ✅ 레이어 분리 정확성 확인")
        print("  ✅ 데이터 흐름 정확성 확인")
        print("  ✅ 알고리즘 정확성 확인")
        print("\n🎯 배포 준비도: 완료 ✅")
        print("   엔진은 프로덕션 배포 준비가 완료되었습니다.")
    else:
        print("\n❌ 일부 테스트가 실패했습니다.")
        print(f"   실패: {len(result.failures)}개, 에러: {len(result.errors)}개")
        print("\n⚠️ 배포 전에 모든 테스트를 통과시켜야 합니다.")
    
    print("\n" + "=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

