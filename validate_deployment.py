#!/usr/bin/env python3
"""
Docker Deployment Validation Script
Tests that the Docker setup is ready for deployment.
"""
import os
import subprocess
import sys
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def check_file(filepath, required=True):
    """Check if a file exists."""
    exists = Path(filepath).exists()
    status = "[OK]" if exists else "[MISS]"
    print(f"{status} {filepath}: {'EXISTS' if exists else 'MISSING'}")
    if required and not exists:
        print(f"   WARNING: Required file is missing!")
        return False
    return True


def check_env_file():
    """Check .env file for API key."""
    print_header("Checking Environment Configuration")

    if not Path(".env").exists():
        print("[FAIL] .env file not found")
        print("   Create a .env file with: GOOGLE_API_KEY=your_key_here")
        return False

    with open(".env") as f:
        content = f.read()
        if "GOOGLE_API_KEY" in content and "your_key_here" not in content.lower():
            print("[OK] .env file exists with GOOGLE_API_KEY set")
            return True
        else:
            print("[WARN] .env file exists but GOOGLE_API_KEY may not be set correctly")
            return False


def check_docker():
    """Check if Docker is installed and running."""
    print_header("Checking Docker Installation")

    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"[OK] Docker installed: {result.stdout.strip()}")

            # Check if Docker daemon is running
            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("[OK] Docker daemon is running")
                return True
            else:
                print("[FAIL] Docker daemon is not running")
                print("   Start Docker Desktop or Docker service")
                return False
        else:
            print("[FAIL] Docker not found")
            return False
    except FileNotFoundError:
        print("[FAIL] Docker not installed")
        print("   Install from: https://www.docker.com/get-started")
        return False
    except subprocess.TimeoutExpired:
        print("[FAIL] Docker command timed out")
        return False


def check_docker_compose():
    """Check if Docker Compose is available."""
    try:
        result = subprocess.run(
            ["docker-compose", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"[OK] Docker Compose installed: {result.stdout.strip()}")
            return True
        else:
            # Try docker compose (v2 syntax)
            result = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"[OK] Docker Compose v2 installed: {result.stdout.strip()}")
                return True
            print("[WARN] Docker Compose not found (optional)")
            return False
    except FileNotFoundError:
        print("[WARN] Docker Compose not installed (optional)")
        return False


def check_deployment_files():
    """Check all deployment-related files."""
    print_header("Checking Deployment Files")

    required_files = [
        "Dockerfile",
        "docker-compose.yml",
        ".dockerignore",
        "requirements.txt",
        "app.py",
        "analyzer.py",
        "scraper.py",
        "models.py",
        "logger.py"
    ]

    optional_files = [
        ".streamlit/config.toml",
        "DOCKER_DEPLOYMENT.md",
        "README.md"
    ]

    all_good = True

    print("Required files:")
    for file in required_files:
        if not check_file(file, required=True):
            all_good = False

    print("\nOptional files:")
    for file in optional_files:
        check_file(file, required=False)

    return all_good


def test_docker_build():
    """Test if Docker image can be built."""
    print_header("Testing Docker Build (This may take a few minutes)")

    answer = input("Build Docker image now? This will take ~2-5 minutes. (y/N): ")
    if answer.lower() != 'y':
        print("[SKIP] Skipping Docker build test")
        return None

    print("\nBuilding Docker image...")
    try:
        result = subprocess.run(
            ["docker", "build", "-t", "website-auditor-test", "."],
            timeout=600,  # 10 minute timeout
            capture_output=False  # Show output in real-time
        )

        if result.returncode == 0:
            print("\n[OK] Docker image built successfully!")
            print("\nYou can now run it with:")
            print("  docker run -p 8501:8501 -e GOOGLE_API_KEY=your_key website-auditor-test")
            return True
        else:
            print("\n[FAIL] Docker build failed")
            return False
    except subprocess.TimeoutExpired:
        print("\n[FAIL] Docker build timed out (took longer than 10 minutes)")
        return False
    except KeyboardInterrupt:
        print("\n[WARN] Build cancelled by user")
        return False


def main():
    """Run all deployment validation checks."""
    print_header("Docker Deployment Validation")
    print("This script checks if your project is ready for Docker deployment.\n")

    results = {
        "Files": check_deployment_files(),
        "Environment": check_env_file(),
        "Docker": check_docker(),
        "Docker Compose": check_docker_compose(),
    }

    # Build test (optional)
    build_result = test_docker_build()
    if build_result is not None:
        results["Docker Build"] = build_result

    # Summary
    print_header("Validation Summary")

    for check, passed in results.items():
        status = "[PASSED]" if passed else "[FAILED]"
        print(f"{status}: {check}")

    critical_checks = ["Files", "Environment", "Docker"]
    all_critical_passed = all(results.get(check, False) for check in critical_checks)

    if all_critical_passed:
        print("\n*** All critical checks passed! You're ready to deploy. ***")
        print("\nNext steps:")
        print("  1. Build and run locally:")
        print("     docker-compose up -d")
        print("\n  2. Or deploy to cloud:")
        print("     See DOCKER_DEPLOYMENT.md for platform-specific instructions")
        return 0
    else:
        print("\n*** Some critical checks failed. Please fix the issues above. ***")
        print("\nRequired for deployment:")
        for check in critical_checks:
            status = "[OK]" if results.get(check, False) else "[FAIL]"
            print(f"  {status} {check}")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[WARN] Validation cancelled by user")
        sys.exit(1)
