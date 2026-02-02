#!/usr/bin/env python3
"""
우울증 시뮬레이션 실행 스크립트

메인 실행 파일
"""

import sys
import os
from pathlib import Path

# 패키지 경로 추가
sys.path.insert(0, str(Path(__file__).parent))

from brain_disorder_simulation.disorders.depression.depression_simulator import main

if __name__ == "__main__":
    main()

