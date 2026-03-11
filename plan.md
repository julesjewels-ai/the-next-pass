1. Modify `tests/test_main.py`
   - Move the imports to the top of the file to fix ruff errors (E402).
   - Ensure the new tests for `handle_translate`, `handle_match`, `main_dispatch_commands`, `main_invalid_command`, and `main_no_args` are correctly added to achieve full branch coverage (except the `if __name__ == '__main__':` block, line 196) and follow the type hinting constraints.

2. Run validation gates
   - Run `pytest --cov=. --cov-branch --cov-report=term-missing` (Must Pass).
   - Run `mypy .` (Must Pass - Zero Errors).
   - Run `ruff check .` (Must Pass).
   - Run `sudo apt-get install -y graphviz` then verify `dot -V`.
   - Run `pydeps . --noshow` (Must Pass), then delete the generated `app.svg` and `src.svg`.

3. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

4. Output `<promise>COMPLETE</promise>`
