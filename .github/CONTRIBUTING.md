# Contribution Guidelines

Thank you for considering contributing! We welcome contributions in the form of bug reports, feature requests, code patches, or documentation improvements.

Please follow these guidelines to ensure a smooth contribution process.

## Bug Reports

If you've found a bug, please create a bug report. Make sure to provide the following information:

- **Environment Information:** (e.g., Home Assistant version, HA Toyota version)
- **Steps to Reproduce the Bug:**
- **Expected Behavior:**
- **Current Behavior:**

## Feature Requests

If you have an idea for a new feature, please create a feature request. Describe the desired feature and why it would be useful.

## Code Contributions

We welcome code contributions! If you'd like to participate in development, follow these steps:

1. Fork this repository.
2. Create a branch for your changes: e.g `git checkout -b feature/feature_description` or `git checkout -b bug/bug_description`.
3. Develop and test your changes.
4. Ensure your code complies with style guidelines: `poetry run pre-commit run --all-files`.
5. Create a pull request in this repository with a clear description of the changes.

### Development Requirements

- Dependencies are managed with [Poetry](https://python-poetry.org/). Add new dependencies to the `pyproject.toml` file and run `poetry install`.
- Style guidelines are enforced with [pre-commit](https://pre-commit.com/). Install pre-commit with `poetry run pre-commit install`.

### Tests

Ensure that all tests pass successfully before creating a pull request.

```bash
poetry run pytest
```
