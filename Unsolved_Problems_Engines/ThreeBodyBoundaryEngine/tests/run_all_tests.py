"""
모든 테스트 실행

Author: GNJz (Qquarts)
Version: 1.2.0
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def run_all_tests():
    """모든 테스트 실행"""
    print("=" * 60)
    print("ThreeBodyBoundaryEngine - 전체 테스트 실행")
    print("=" * 60)
    
    test_files = [
        "test_three_body_boundary_engine.py",
        "test_gravity_calculator.py",
        "test_boundary_convergence.py",
        "test_integration.py"
    ]
    
    passed = 0
    failed = 0
    
    for test_file in test_files:
        test_path = Path(__file__).parent / test_file
        if test_path.exists():
            print(f"\n{'=' * 60}")
            print(f"실행 중: {test_file}")
            print('=' * 60)
            
            try:
                # 테스트 파일을 모듈로 실행
                import importlib.util
                spec = importlib.util.spec_from_file_location("test_module", test_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # main 함수가 있으면 실행
                if hasattr(module, 'main'):
                    module.main()
                elif hasattr(module, 'run_all_tests'):
                    success = module.run_all_tests()
                    if not success:
                        failed += 1
                        continue
                
                passed += 1
                print(f"✅ {test_file}: 통과")
            except Exception as e:
                failed += 1
                print(f"❌ {test_file}: 실패 - {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"⚠️ {test_file}: 파일 없음")
    
    print("\n" + "=" * 60)
    print(f"전체 테스트 결과: {passed}개 통과, {failed}개 실패")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

