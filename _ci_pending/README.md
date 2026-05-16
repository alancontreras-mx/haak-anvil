# CI Workflow (pending activation)

The GitHub Actions workflow `ci.yml` is staged here while we wait for the
`workflow` OAuth scope to be granted to the GitHub CLI used during initial
upload.

To activate it:

```bash
# 1) Grant the workflow scope to gh:
gh auth refresh -s workflow

# 2) Move the file into place:
mkdir -p .github/workflows
mv _ci_pending/ci.yml .github/workflows/ci.yml
rmdir _ci_pending

# 3) Commit and push:
git add .github/workflows/ci.yml
git commit -m "ci: enable GitHub Actions matrix (Linux/Mac/Windows x py3.10-3.12)"
git push
```

The workflow runs lint (ruff), tests (pytest with coverage) and builds the
wheel + sdist on every push and PR to `main`.
