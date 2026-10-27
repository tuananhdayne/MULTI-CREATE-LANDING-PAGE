#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add backend directory to sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.harness.cli import main

if __name__ == "__main__":
    # Default to writing benchmark report if not explicitly provided
    if "--report" not in sys.argv:
        report_dest = Path(__file__).resolve().parent.parent / "docs" / "benchmarks" / "benchmark_latest.md"
        sys.argv.extend(["--report", str(report_dest)])

    main()
