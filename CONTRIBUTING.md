# Contributing to handy-fingers-connorcampagna

Thanks for your interest in contributing! 🖐️✨

This project values **clean code, testability, and thoughtful design**. Please follow these guidelines to keep the codebase maintainable and fun to work with.

---

## 🛠️ Development Setup

1. **Fork and clone** the repository:

   ```bash
   git clone https://github.com/connorcampagna/handy-fingers-connorcampagna.git
   cd handy-fingers-connorcampagna
   ```

2. **Install in editable mode with dev dependencies**:

   ```bash
   pip install -e ".[dev]"
   ```

3. **Run tests** to verify setup:

   ```bash
   make test
   ```

---

## 📜 Style Guidelines

### Python Code

- **Python version**: 3.11+ required.
- **Type hints**: Use them everywhere. The codebase is fully typed.
- **Docstrings**: All public functions, classes, and modules must have docstrings (Google or NumPy style).
- **Line length**: Max 100 characters (enforced by black).

### Formatting

Format your code before committing:

```bash
make format
```

This runs:
- **black**: Automatic code formatting.
- **isort**: Import sorting.

### Linting

Check code quality:

```bash
make lint
```

This runs **ruff** (fast Python linter). Fix all issues before submitting a PR.

---

## 🧪 Testing

**All new features must include tests.**

- Place tests in `tests/` with filenames like `test_<module>.py`.
- Use **pytest** fixtures for reusable test data.
- Run tests with:

  ```bash
  make test
  ```

- Check coverage:

  ```bash
  make test-cov
  ```

### Test Philosophy

- **Unit tests**: Test pure logic (e.g., `fingers.py` ASL recognition) with synthetic data.
- **Integration tests**: Test wiring (e.g., `app.py` with `--no-video`).
- **Fixtures**: Use `tests/assets/` for deterministic landmark data.

---

## 🚦 Pull Request Workflow

1. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes**:
   - Write code with type hints and docstrings.
   - Add tests for new functionality.
   - Update `CHANGELOG.md` under `[Unreleased]`.

3. **Format and lint**:

   ```bash
   make format
   make lint
   ```

4. **Run tests**:

   ```bash
   make test
   ```

5. **Commit with clear messages**:

   ```bash
   git commit -m "feat: add gesture debouncing for spell mode"
   ```

   Use conventional commit prefixes:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation
   - `test:` Tests
   - `refactor:` Code restructuring
   - `perf:` Performance improvement
   - `chore:` Tooling/config

6. **Push and open a PR**:

   ```bash
   git push origin feature/your-feature-name
   ```

   Open a PR on GitHub with:
   - Clear description of changes.
   - Link to related issues (if any).
   - Screenshots/GIFs for UI changes.

---

## 🐛 Reporting Issues

Found a bug? Open an issue with:
- **Description**: What went wrong?
- **Steps to reproduce**: Minimal example.
- **Environment**: OS, Python version, camera model.
- **Expected vs. actual behavior**.

---

## 💡 Feature Requests

Have an idea? Open an issue with:
- **Use case**: Why is this useful?
- **Proposed solution**: How might it work?
- **Alternatives considered**: Other approaches you thought about.

---

## 🎨 Code of Conduct

Be respectful, inclusive, and constructive. We're here to build cool stuff together.

---

## 🙏 Thank You!

Every contribution—code, docs, bug reports, ideas—makes this project better. Appreciate you! 🖐️

---

**Questions?** Open a discussion or reach out to [@connorcampagna](https://github.com/connorcampagna).
