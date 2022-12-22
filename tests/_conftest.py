import subprocess
import sys
from tqdm import tqdm


def pytest_configure(config):
    print("Building project...")
    with tqdm(total=1, desc="Building project", file=sys.stdout) as pbar:
        subprocess.run(["poetry", "build"])
        pbar.update(1)
    print("Installing project...")
    with tqdm(total=1, desc="Installing project", file=sys.stdout) as pbar:
        subprocess.run(["pip", "install", "--force", "--find-links=dist", "codegpt"])
        pbar.update(1)
    print("Installation complete.")


if __name__ == "__main__":
    pytest_configure({})
