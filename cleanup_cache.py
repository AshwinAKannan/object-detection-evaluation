import os
import shutil


def cleanup_cache_and_pycache(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            # Check for and remove __pycache__ and .pytest_cache directories
            if dir_name == '__pycache__' or dir_name == '.pytest_cache':
                cache_dir = os.path.join(root, dir_name)
                print(f"Removing {cache_dir}")
                shutil.rmtree(cache_dir)


if __name__ == "__main__":
    cleanup_cache_and_pycache(".")