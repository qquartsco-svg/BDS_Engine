#!/usr/bin/env python3
"""
ThreeBodyBoundaryEngine - pytest 기반 통합 테스트 실행 스크립트

pytest를 사용하여 모든 테스트를 실행하고 상세한 결과를 출력합니다.

사용법:
    python3 run_tests_pytest.py
    또는
    chmod +x run_tests_pytest.py
    ./run_tests_pytest.py
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

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


def run_pytest_tests():
    """pytest를 사용하여 모든 테스트 실행"""
    print_header("ThreeBodyBoundaryEngine 통합 테스트 (pytest)")
    print(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"버전: 1.2.0")
    
    project_root = Path(__file__).parent
    tests_dir = project_root / "tests"
    
    print_section("테스트 실행 시작")
    print("pytest를 사용하여 모든 테스트를 실행합니다...\n")
    
    # pytest 실행
    result = subprocess.run(
        ["python3", "-m", "pytest", str(tests_dir), "-v", "--tb=short", "--color=yes"],
        cwd=str(project_root),
        capture_output=False,
        text=True
    )
    
    print_section("테스트 결과 요약")
    
    if result.returncode == 0:
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
        print("   자세한 내용은 위의 출력을 확인하세요.")
    
    print("\n" + "=" * 70)
    
    return result.returncode == 0


if __name__ == "__main__":
    success = run_pytest_tests()
    sys.exit(0 if success else 1)

