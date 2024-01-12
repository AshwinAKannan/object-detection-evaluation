import os


def cleanup_pycache(root_dir) -> None:
    for root, dirs, files in os.walk(top=root_dir):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_dir = os.path.join(root, dir_name)
                print(f"Removing {pycache_dir}")
                for item in os.listdir(pycache_dir):
                    item_path = os.path.join(pycache_dir, item)
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                os.rmdir(pycache_dir)


if __name__ == "__main__":
    cleanup_pycache(root_dir=".")
