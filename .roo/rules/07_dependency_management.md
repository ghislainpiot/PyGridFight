# Dependency Management

## UV Tool Usage
- All Python package dependencies must be managed using the `uv` command-line tool
- Use `uv pip install <package>` and `uv pip uninstall <package>` for dependency management
- Do not manually edit `pyproject.toml` dependency sections or `requirements.txt` for dependency management

## Dependency Control
- Dependencies should be pinned to specific versions in `pyproject.toml` for stability
- Use exact versions (e.g., `package_name=="1.2.3"`) or compatible release specifiers (e.g., `package_name>=1.2.0,<1.3.0`)
- Generate and commit lock files to the repository
- Lock files should only be updated when dependencies are intentionally changed

## Dependency Review Process
- Adding new dependencies should be done thoughtfully
- Consider impact on project size, security, and maintenance
- Discuss significant or controversial dependencies with the team
- Regularly review and update dependencies to latest stable versions
- Test thoroughly after dependency updates