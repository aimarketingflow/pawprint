# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Reporting a Vulnerability

We take the security of the Pawprinting PyQt6 V2 application seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do not disclose the vulnerability publicly**
2. **Email us** at security@example.com with details about:
   - The specific vulnerability
   - Steps to reproduce
   - Potential impact
   - (Optional) Any suggested fixes
3. **Allow time for response** - We aim to acknowledge receipt within 48 hours and provide a more detailed response within 5 business days
4. **Coordinate disclosure** - We will work with you to fix the issue and coordinate disclosure

## Security Considerations

The Pawprinting PyQt6 V2 application operates primarily as a local desktop application. However, there are several security considerations:

1. **Local File Access** - The application accesses local files for pawprinting and comparison
2. **No Network Activity** - By default, the application does not send or receive data over networks
3. **External Libraries** - We depend on various open-source libraries that may have their own security issues

## Security Features

The Pawprinting PyQt6 V2 application includes:

1. **File Integrity Checks** - For pawprint verification
2. **Secure Storage** - For configuration and history data
3. **Input Validation** - For all file operations

Thank you for helping keep our project secure!
