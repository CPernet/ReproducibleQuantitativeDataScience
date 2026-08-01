# Agent instructions

## Repository structure

- Source code is under `src/`.
- Tests are under `tests/`.
- Instructions (README) is at the root`.

## Testing

- Use `pytest`.
- Name test files `test_<module>.py`.
- Prefer parametrized tests for related cases.
- Use `numpy.testing.assert_allclose` for numerical arrays.
- Every bug fix must include a regression test.
