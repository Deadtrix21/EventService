import sys
import pytest
import os

def main():
    """
    Main entry point to run all tests in the ServiceTools.tools package.
    """
    # Run all tests in the current working directory
    exit_code = pytest.main([
         os.path.join(os.getcwd(), "tools/tests"),
        "-v"
    ])
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
