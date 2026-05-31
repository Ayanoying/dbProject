from pathlib import Path
import sys


# Allows us to import from the src directory, which is where our dbInitialisation module is located
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from dbInitialisation import init_data


def main():
    init_data()


if __name__ == "__main__":
    main()
