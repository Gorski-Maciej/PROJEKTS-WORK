from __future__ import annotations

import subprocess
from pathlib import Path


def commit_config_change(repo_root: str, file_path: str, message: str) -> bool:
    full = Path(repo_root) / file_path
    if not full.exists():
        return False

    add = subprocess.run(['git', '-C', repo_root, 'add', file_path], check=False)
    if add.returncode != 0:
        return False

    diff = subprocess.run(['git', '-C', repo_root, 'diff', '--cached', '--quiet'], check=False)
    if diff.returncode == 0:
        return False

    commit = subprocess.run(['git', '-C', repo_root, 'commit', '-m', message], check=False)
    return commit.returncode == 0
