# Contributing

Keep notes searchable, reproducible and attributed. Use [the technique template](templates/technique.md) for new material and update [coverage](docs/coverage.md).

- Explain when a technique applies, where commands run and what output establishes success.
- Use synthetic addresses/names; never commit private evidence, credentials or restricted exam material.
- Link primary documentation and record review date and tool version when known.
- Distinguish draft, source-reviewed and lab-tested content. Do not infer lab validation from a successful syntax check.
- Label training-only tools and restricted features at the point of use.
- Preserve existing attribution; do not copy unlicensed material or add a blanket license over third-party contributions without checking rights.
- Keep scripts small, transparent and offline unless their networking behavior is explicitly documented.
- Use Conventional Commits for commit messages and PR titles: `docs: clarify pivoting prerequisites`, `fix: handle an existing notebook`, or `feat: add a study helper`.

Before submitting:

```bash
python3 scripts/check_docs.py
python3 -m unittest discover -s tests -v
git diff --check
```

The documentation checker verifies local inline Markdown file paths and ordinary heading/explicit-anchor fragments. It does not certify external links, arbitrary Markdown dialects, tool correctness or exam permission. When moving a section, preserve its old README bookmark or update links and add a compatibility entry. Mark constructed output as illustrative; reserve target-lab-tested status for a dated record in [validation](docs/lab-validation.md).
