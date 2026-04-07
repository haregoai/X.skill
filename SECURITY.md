# Security

## Scope

This repository is designed to stay public-safe by keeping private memory and runtime state outside version control.

## Please Report

Report an issue if you find:

- a path that leaks personal machine layout
- a committed secret, token, or auth artifact
- generated runtime files that should be ignored
- sample data that appears to contain real personal content
- docs that encourage unsafe publishing practices

## Sensitive Data Policy

Never open a public issue containing:

- API keys or tokens
- cookies or browser session data
- private memory contents
- personal account identifiers that are not already intentionally public

If a security issue includes sensitive data, report it privately to the maintainer instead of posting it in a public issue.

## Hardening Rule

When in doubt, remove the data from the repository and replace it with a template, mock example, or config field.
