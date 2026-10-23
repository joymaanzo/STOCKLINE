# Development Process

## Roles

- **PM:** Grooms the issue.
- **Engineer:** Implements one issue.
- **QA:** Checks the implementation against the acceptance criteria.

## Lifecycle

1. Pick the next open issue.
2. The engineer implements it.
3. QA checks every acceptance criterion and posts `QA: PASS` or `QA: FAIL` as an issue comment.
4. On `QA: FAIL`, the engineer fixes the issue using that comment.
5. On `QA: PASS`, the issue is closed.