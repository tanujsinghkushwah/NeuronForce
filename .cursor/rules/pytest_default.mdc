---
description: Require pytest for all test cases.
globs: ["backend/tests/**.py", "tests/**.py"]
alwaysApply: true
---

# Pytest Rule

- Use `pytest` for all test cases and test-related code suggestions.
- Do not use `unittest` or other test libraries.
- Utilize pytest features such as fixtures, mocks, and parametrization.
- Organize tests in the `backend/tests/` directory with descriptive, consistent naming (`test_*.py`).
- Example:
    ```python
    import pytest

    def test_addition():
        assert 1 + 1 == 2
    ```
- Before running the test cases, activate the virtual environment first using `source backend/venv/bin/activate` and export the PYTHONPATH using `export PYTHONPATH=$PYTHONPATH:$(pwd)/backend`.
