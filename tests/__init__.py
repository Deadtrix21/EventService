
import pytest
import os
import sys

def main():
    exit_code = pytest.main([os.path.dirname(__file__), "-v"])
    sys.exit(exit_code)

if __name__ == "__main__":
    main()