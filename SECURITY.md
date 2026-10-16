# Security Policy

## Scope

SENTINEL is an educational network-traffic monitoring and anomaly-detection project. Its current machine-learning model is experimental and uses synthetic training data; it is not a certified intrusion-detection product and cannot guarantee accurate detection.

## Supported Versions

Security fixes are generally intended for the latest version on the default branch. No formal long-term support policy is currently defined.

## Reporting a Vulnerability

Please do not publish passwords, tokens, private packet captures, personal data, or a working exploit in a public issue.

Until a private security-reporting channel is configured, contact the repository owner through a contact method listed on the owner's GitHub profile. Include:
- A concise description of the issue.
- The potential impact.
- Steps to reproduce using a safe, authorized test environment.
- Any suggested mitigation.

Please allow reasonable time to investigate before publicly disclosing a confirmed vulnerability.

## Safe and Authorized Use

- Monitor only devices and networks you own or are explicitly authorized to monitor.
- Treat captured traffic and IP addresses as potentially sensitive data.
- Keep logs and database files private when they contain identifying network information.
- Do not commit credentials, `.env` files, private captures, or sensitive logs.
- Run the application with only the permissions it needs.
- Do not rely on SENTINEL alone to make security decisions.

This policy is a starting point and may be updated as the project develops.
