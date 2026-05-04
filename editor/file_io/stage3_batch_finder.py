"""Discover deterministic Stage 3 batch files under a root directory."""

from pathlib import Path


def discover_stage3_batch_files(root_dir: Path) -> list[Path]:
    """Return recursively discovered `batch-*.json` files under `root_dir`."""
    if not root_dir.exists():
        raise FileNotFoundError(root_dir)
    if not root_dir.is_dir():
        raise NotADirectoryError(root_dir)

    batch_files = [
        path
        for path in root_dir.rglob("batch-*.json")
        if path.is_file() and not any(part.startswith(".") for part in path.relative_to(root_dir).parts)
    ]
    return sorted(batch_files, key=lambda path: path.relative_to(root_dir).as_posix())