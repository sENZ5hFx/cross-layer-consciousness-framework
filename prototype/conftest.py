# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
# conftest.py — pytest sys.path bootstrap. Auto-loaded by pytest before any test.
import sys
import os

# Ensure prototype/ itself is on sys.path so subsystem1/2/3 and embeddings resolve
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# Also add repo root in case anything imports from there
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
