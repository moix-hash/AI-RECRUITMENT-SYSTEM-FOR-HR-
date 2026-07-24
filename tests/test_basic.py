from pathlib import Path


def test_project_structure_exists() -> None:
    root = Path(__file__).resolve().parents[1]
    expected_paths = [
        root / "app",
        root / "ai",
        root / "components",
        root / "database",
        root / "pages",
        root / "utils",
        root / "requirements.txt",
        root / "README.md",
    ]
    for path in expected_paths:
        assert path.exists(), f"Missing expected path: {path}"
