import sys
import os
WORK_PATH = os.path.dirname(os.path.realpath(__file__))
WORK_PATH = os.path.dirname(WORK_PATH)
if not WORK_PATH in sys.path:
    sys.path.append(WORK_PATH)
