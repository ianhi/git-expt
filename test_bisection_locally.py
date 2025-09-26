#!/usr/bin/env python3
"""
Local testing script for the bisection feature.
"""
import os
import subprocess
import sys
import tempfile
import json
from pathlib import Path

# Add the issue-from-pytest-log-action directory to Python path
action_path = Path("/Users/ian/Documents/dev/issue-from-pytest-log-action")
sys.path.insert(0, str(action_path))

try:
    import track_packages
    import parse_logs
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure the path to issue-from-pytest-log-action is correct")
    sys.exit(1)


def run_tests_and_generate_log():
    """Run pytest and generate a log file."""
    print("Running pytest to generate log...")
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "test_sample.py",
        "--report-log=pytest-log.jsonl",
        "-v"
    ], capture_output=True, text=True)

    print(f"Pytest exit code: {result.returncode}")
    print(f"Pytest stdout:\n{result.stdout}")
    if result.stderr:
        print(f"Pytest stderr:\n{result.stderr}")

    return "pytest-log.jsonl"


def test_package_tracking():
    """Test the package tracking functionality."""
    print("\n=== Testing Package Tracking ===")

    # Test getting current package versions
    packages = ["numpy", "pytest", "requests"]
    versions = track_packages.get_current_package_versions(packages)
    print(f"Current package versions: {versions}")

    # Test getting all packages
    all_packages = track_packages.get_all_installed_packages()
    print(f"Total packages installed: {len(all_packages)}")
    print(f"Sample packages: {dict(list(all_packages.items())[:5])}")

    # Test git info
    git_info = track_packages.get_git_info()
    print(f"Git info: {git_info}")


def test_log_parsing(log_file):
    """Test parsing the pytest log."""
    print(f"\n=== Testing Log Parsing ===")

    if not os.path.exists(log_file):
        print(f"Log file {log_file} not found")
        return

    # Test extracting failed tests
    failed_tests = track_packages.extract_failed_tests_from_log(log_file)
    print(f"Failed tests: {failed_tests}")

    # Test creating bisection data
    packages = ["numpy", "pytest", "requests"]
    bisect_data = track_packages.create_bisect_data(packages, log_file)
    print(f"Bisection data created:")
    print(json.dumps(bisect_data, indent=2))


def test_bisection_comparison():
    """Test the bisection comparison functionality."""
    print(f"\n=== Testing Bisection Comparison ===")

    # Create mock data for testing
    packages = ["numpy", "pytest", "requests"]
    current_data = track_packages.create_bisect_data(packages, "pytest-log.jsonl")

    # Create mock previous data (simulating a previous successful run)
    previous_data = {
        "workflow_run_id": "12345",
        "timestamp": "2024-01-01T00:00:00Z",
        "python_version": "3.11.0",
        "packages": {
            "numpy": "1.24.0",  # Different version
            "pytest": "7.4.0",
            "requests": "2.31.0"
        },
        "failed_tests": [],
        "test_status": "passed",
        "git": {
            "commit_hash": "abc123def456",
            "commit_hash_short": "abc123de",
            "commit_message": "Previous commit message",
            "commit_author": "Test Author",
            "commit_date": "2024-01-01 00:00:00"
        }
    }

    # Generate comparison (note: this would normally query the branch)
    # For local testing, we'll just simulate
    comparison = track_packages.format_bisect_comparison(
        current_data, previous_data, "test-branch"
    )

    if comparison:
        print("Generated bisection comparison:")
        print(comparison)
    else:
        print("No comparison generated (no failed tests)")


def main():
    """Main test function."""
    print("=== Local Bisection Testing ===")

    # Test package tracking
    test_package_tracking()

    # Run tests and generate log
    log_file = run_tests_and_generate_log()

    # Test log parsing
    test_log_parsing(log_file)

    # Test bisection comparison
    test_bisection_comparison()

    print("\n=== Testing Complete ===")


if __name__ == "__main__":
    main()