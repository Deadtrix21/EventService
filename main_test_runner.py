import sys
import pytest

def main():
    """
    Main entry point to run all tests in the ServiceTools.tools package.
    """
    # Run all tests in the tools/tests directory
    exit_code = pytest.main([
        "C:/Signiflow.Scripts/PythonProject/ServiceTools/tools/tests",
        "-v"
    ])
    sys.exit(exit_code)

if __name__ == "__main__":
    main()

