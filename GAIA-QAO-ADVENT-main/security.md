# GAIA-QAO-AdVent Security Policy

The GAIA-QAO Consortium takes the security of our systems very seriously. We appreciate the efforts of security researchers and the community to help us maintain a high standard of security and safety for our aerospace and quantum computing platform.

This document outlines our security policy and the procedure for responsibly reporting vulnerabilities.

## Table of Contents

1.  [Supported Versions](#supported-versions)
2.  [Reporting a Vulnerability](#reporting-a-vulnerability)
3.  [Our Commitment (The Process)](#our-commitment-the-process)
4.  [Scope](#scope)
5.  [Out of Scope](#out-of-scope)
6.  [Safe Harbor](#safe-harbor)

## Supported Versions

Due to the rapid development and mission-critical nature of our software, only the latest major release and the current `develop` branch receive security support.

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| 1.x.x   | :x:                |
| < 1.0   | :x:                |

Please ensure you are testing against the latest version before submitting a report.

## Reporting a Vulnerability

**DO NOT report security vulnerabilities through public GitHub issues.**

To ensure the confidentiality of your finding, please report any suspected security vulnerabilities directly to our dedicated security team via email:

**security@gaia-qao.org**

You can encrypt your message using our PGP key:

```
-----BEGIN PGP PUBLIC KEY BLOCK-----

(Aquí iría el bloque de clave pública PGP completo del equipo de seguridad de GAIA-QAO)
Comment: GAIA-QAO Security Team <security@gaia-qao.org>
Version: GnuPG v2

mQINBF...
...
...
=W4pE
-----END PGP PUBLIC KEY BLOCK-----
```

Please include the following information in your report:

-   **A clear and concise description** of the vulnerability.
-   The **component or module** affected (e.g., `api-gateway`, `Q-AIR/BWBQ100`, `Q-SPACE/STS-100`).
-   **Step-by-step instructions** to reproduce the issue, including any scripts, code, or configurations.
-   The **potential impact** of the vulnerability (e.g., data exfiltration, denial of service, unauthorized system control).
-   Any **suggested mitigations** or fixes, if you have them.

## Our Commitment (The Process)

When you report a vulnerability to us, we commit to the following process:

1.  **Acknowledgement:** We will acknowledge receipt of your report within **48 business hours**.
2.  **Initial Triage:** Our security team will triage the vulnerability to determine its validity and severity within **5 business days**.
3.  **Communication:** We will maintain an open channel of communication with you, providing updates on our progress as we work on a fix.
4.  **Resolution:** We will notify you once the vulnerability has been patched. We aim to resolve critical vulnerabilities as quickly as possible.
5.  **Public Disclosure & Recognition:** With your permission, we will publicly credit you for your discovery in the security advisory and release notes once the vulnerability is fixed and disclosed. We typically follow a 90-day disclosure deadline.

## Scope

The following systems and assets are considered **in scope** for our security policy:

-   All source code within this repository (`gaia-qao/gaia-qao-advent`).
-   Publicly exposed API endpoints associated with our official deployments.
-   The infrastructure configuration defined in the `/kubernetes` directory.

## Out of Scope

The following are considered **out of scope**:

-   Denial of Service (DoS/DDoS) attacks against our infrastructure. Please do not perform any testing that could disrupt our services.
-   Social engineering or phishing attacks against GAIA-QAO Consortium members.
-   Physical security of our facilities.
-   Vulnerabilities in third-party dependencies (please report them to the respective project maintainers).

## Safe Harbor

We consider security research and responsible disclosure conducted under this policy to be authorized and beneficial. We will not pursue or support any legal action against you for a vulnerability report that complies with this policy. We will work with you to understand and resolve the issue quickly, and we will not engage in legal action for accidental, good-faith violations of this policy.

---

**GAIA-QAO Consortium Security Team**

