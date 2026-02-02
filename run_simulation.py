#!/usr/bin/env python3
"""
뇌 질환 시뮬레이션 실행 스크립트

메인 실행 파일
"""

import sys
import os
from pathlib import Path

# 패키지 경로 추가
sys.path.insert(0, str(Path(__file__).parent))

# Cookiie Brain Engine 경로 설정
cookiie_brain_path = os.getenv('COOKIIE_BRAIN_PATH', 
                                str(Path(__file__).parent.parent / 'Cookiie_Brain_Engine'))
sys.path.insert(0, str(Path(cookiie_brain_path) / 'package'))

from brain_disorder_simulation.unified.unified_simulator import main

if __name__ == "__main__":
    main()

