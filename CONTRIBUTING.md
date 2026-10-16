# Contributing to SENTINEL

Thank you for your interest in contributing to SENTINEL — Network Traffic Monitoring & Intrusion Detection System.

## Before You Start

- Read the project's `README.md` to understand its purpose and setup.
- Review `LICENSE` for the terms that apply to contributions and reuse.
- Only test network-monitoring features on systems and networks you own or are explicitly authorized to assess.
- Do not submit private packet captures, credentials, API keys, personal information, or other sensitive data.

## How to Contribute

1. **Fork** the repository on GitHub.
2. **Clone** your fork to your computer.
3. Create a branch for your change:
   ```bash
   git checkout -b feature/short-description
   ```
4. Set up the Python environment and install dependencies as described in `README.md`.
5. Make a focused change and add or update tests where appropriate.
6. Run the relevant tests and confirm they pass.
7. Review your changes for secrets, private data, and unrelated files.
8. Commit and push your branch:
   ```bash
   git add .
   git commit -m "Describe the change"
   git push origin feature/short-description
   ```
9. Open a Pull Request against the original repository and explain what changed, why it helps, and how you tested it.

## Contribution Guidelines

- Keep changes focused and use clear names.
- Follow the existing code style where practical.
- Explain important behavior in comments or documentation when it is not obvious.
- Never claim that an alert proves an intrusion. The current machine-learning model is experimental and may produce false positives or false negatives.
- Do not add functionality intended for unauthorized access, stealth, credential theft, or disruption of networks.

## Reporting Bugs

When reporting a bug, include:
- Operating system and Python version.
- Steps to reproduce the problem.
- Expected behavior and actual behavior.
- Relevant error messages with secrets and private network details removed.

## Suggesting Features

Describe the use case, the expected benefit, and any security or privacy implications.

Thank you for helping improve SENTINEL!
