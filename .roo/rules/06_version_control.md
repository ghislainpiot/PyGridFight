# Version Control Practices

## Commit Messages
- All commit messages must adhere to the Conventional Commits specification
- Common types include: `feat`, `fix`, `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`
- Examples: `feat: add new avatar purchase endpoint`, `fix: correct score calculation for ties`, `docs: update architecture diagram for scoring`

## Commit Quality
- Commits should be atomic and represent a single logical change
- Avoid bundling unrelated changes into one commit
- All tests must pass before code is committed to the main development branch
- Committing code that breaks tests is not allowed

## Branching Strategy
- Development will primarily occur directly on the main branch (trunk-based development)
- Short-lived feature branches may be used for larger changes that cannot be completed quickly
- Merge back to the trunk frequently (ideally multiple times a day, or at least daily)
- All code merged to the trunk must be production-ready and pass all tests

## Commit Message Content
- Beyond the conventional commit type and scope, the commit message body should clearly explain the "what" and "why" of the change, not just the "how"