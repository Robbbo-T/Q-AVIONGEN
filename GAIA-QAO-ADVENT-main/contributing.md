# Contributing to GAIA-QAO-AdVent

First off, thank you for considering contributing to GAIA-QAO-AdVent. This is a complex, mission-critical project, and we value every contribution, from fixing a typo in the documentation to developing a new quantum algorithm.

This document provides guidelines for contributing to the project to ensure a smooth, consistent, and legally sound development process for everyone involved.

## Table of Contents

1.  [Code of Conduct](#code-of-conduct)
2.  [Contributor License Agreement (CLA)](#contributor-license-agreement-cla)
3.  [Getting Started: Your First Contribution](#getting-started-your-first-contribution)
4.  [Development Workflow](#development-workflow)
    - [Branching Strategy](#branching-strategy)
    - [Commit Message Convention](#commit-message-convention)
    - [Code Style and Linting](#code-style-and-linting)
5.  [Submitting a Pull Request (PR)](#submitting-a-pull-request-pr)
    - [PR Title and Description](#pr-title-and-description)
    - [Review Process](#review-process)
6.  [Documentation Standards](#documentation-standards)
7.  [Reporting Bugs and Proposing Features](#reporting-bugs-and-proposing-features)

## Code of Conduct

All contributors are expected to adhere to the [GAIA-QAO Code of Conduct](CODE_OF_CONDUCT.md). Please be respectful and professional in all interactions. We are committed to fostering an open and welcoming environment.

*(Nota: Se asume la existencia de un archivo CODE_OF_CONDUCT.md. Si no existe, esta sección puede simplificarse).*

## Contributor License Agreement (CLA)

Due to the proprietary and safety-critical nature of the GAIA-QAO-AdVent project, all contributors must sign our Contributor License Agreement (CLA) before any code or significant documentation can be merged.

-   **Why a CLA?** The CLA protects you and the GAIA-QAO Consortium. It grants the consortium the necessary rights to use and re-license your contribution under the project's main license while ensuring you retain ownership of your original work. This is a standard practice for large-scale, controlled projects.
-   **How to Sign:** When you open your first Pull Request, a CLA-bot will automatically comment with a link to sign the agreement electronically. This is a one-time process.

**Contributions cannot be accepted until the CLA is signed.**

## Getting Started: Your First Contribution

1.  **Run the Setup Script:** Make sure your local environment is fully configured by running `./scripts/setup.sh`.
2.  **Find an Issue:** Look for issues tagged `good first issue` or `help wanted` in our issue tracker. These are curated to be good entry points into the project.
3.  **Claim the Issue:** Comment on the issue to let others know you are working on it.
4.  **Ask Questions:** If you're unsure about anything, don't hesitate to ask for clarification in the issue comments.

## Development Workflow

We follow a strict development workflow to maintain the quality and traceability of the codebase.

### Branching Strategy

We use a simplified Git-Flow model:

-   `main`: This branch represents the latest stable, production-ready release. Direct commits are strictly forbidden. Merges only happen from the `develop` branch during a release cycle.
-   `develop`: This is the primary development branch. All feature branches are merged into `develop`. It should always be in a state that could potentially be released.
-   **Feature Branches:** All new work must be done on a feature branch.
    -   Branch from the latest `develop`.
    -   Name your branch descriptively using the format: `feature/<issue-id>-<short-description>` (e.g., `feature/T-123-fix-qns-drift`).
    -   For bug fixes: `fix/<issue-id>-<description>`.
    -   For documentation: `docs/<issue-id>-<description>`.

### Commit Message Convention

We enforce the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This helps automate changelog generation and makes the commit history highly readable.

**Format:** `<type>(<scope>): <subject>`

-   **`<type>`:** `feat` (new feature), `fix` (bug fix), `docs` (documentation), `style` (formatting), `refactor`, `test`, `chore` (build/tooling changes).
-   **`<scope>` (optional):** The module affected (e.g., `q-air`, `ata-34`, `api`, `ci`).
-   **`<subject>`:** A concise, imperative-tense description of the change.

**Example:** `feat(ata-34): implement quantum gyroscope drift compensation`
**Example:** `fix(api): correct payload validation for telemetry endpoint`
**Example:** `docs(contributing): clarify CLA signing process`

### Code Style and Linting

-   **Consistency is Key:** Adhere to the coding style of the existing codebase for the language you are working with (e.g., PEP 8 for Python, `rustfmt` for Rust).
-   **Run Linters:** Before committing, run the appropriate linters. This will eventually be automated by our pre-commit hooks.

## Submitting a Pull Request (PR)

### PR Title and Description

-   **Title:** The PR title should follow the Conventional Commits format, as it will be used for the squash-and-merge commit message.
-   **Description:** Use the PR template provided. Clearly describe:
    -   **What** change you made.
    -   **Why** you made it (link to the issue, e.g., "Closes #123").
    -   **How** you tested it.

### Review Process

1.  **Automated Checks:** Once a PR is opened, our CI pipeline will automatically run:
    -   Linting checks.
    -   Unit tests (`scripts/test.sh unit`).
    -   Integration tests (`scripts/test.sh integration`).
    -   CLA-bot verification.
2.  **Code Review:** At least **two** core team members must review and approve the PR.
3.  **Address Feedback:** Respond to comments and push changes to your feature branch. The PR will update automatically.
4.  **Merge:** Once approved and all checks pass, a core team member will squash and merge your PR into the `develop` branch.

## Documentation Standards

-   **Code Comments:** All public functions, complex algorithms, and non-obvious code blocks must be well-commented.
-   **ATA/SSA Chapters:** All contributions to a system must be reflected in its corresponding `ATA-XX` or `SSA-XX` directory, following the lifecycle structure defined in its `README.md`.
-   **Markdown:** All documentation should be written in clean, readable Markdown.

## Reporting Bugs and Proposing Features

-   **Use the Issue Tracker:** All bug reports and feature proposals should be submitted through the GitHub issue tracker.
-   **Use Templates:** Please use the provided "Bug Report" or "Feature Request" templates to ensure you provide all necessary information.

---

Thank you again for your interest in making GAIA-QAO-AdVent a success!
