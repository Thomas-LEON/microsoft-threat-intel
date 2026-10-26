# 🔷 Microsoft Security — Weekly Threat Intel Briefing
**Report Date:** 2026-10-26
**Coverage Period:** 2026-10-19 → 2026-10-26

**Weekly Threat Score:** 86/100
*(Auditable Metrics - Threat Capability: 9/10 | Event Frequency: 8/10 | Business Impact: 9/10)*

---

## Incident Title: LiteLLM 1.107.0 Supply Chain Compromise via Python Startup Hooks — October 23, 2026

**Incident Metadata:**
- **Primary Category:** SUPPLY CHAIN
- **Timeline:** Event: October 23, 2026 | Disclosed: October 23, 2026
- **Impacted Products:** LiteLLM (used within Microsoft AI/LLM development pipelines), Python environments
- **Impacted Country:** Global
- **List of Companies Impacted:** Unknown (Organizations utilizing LiteLLM in AI workflows)

Microsoft Threat Intelligence identified a malicious supply chain compromise within the LiteLLM 1.107.0 package, which is frequently leveraged by developers building AI applications on Microsoft infrastructure. The attack utilized Python startup hooks to facilitate credential theft and remote code execution.

**Overview**
The compromise of LiteLLM 1.107.0 represents a sophisticated supply chain attack targeting the AI development ecosystem. By injecting malicious code into the package, threat actors gained the ability to execute arbitrary commands and exfiltrate sensitive credentials from the environments of developers and automated CI/CD pipelines that pull this dependency.

**Technical Details**
- **Python Startup Hooks:** The attackers leveraged the `sitecustomize.py` or `usercustomize.py` mechanisms, which Python automatically executes upon startup, to ensure the malicious payload runs regardless of the primary application logic.
- **Credential Exfiltration:** The malicious code was designed to scan environment variables and local configuration files for API keys, cloud provider credentials, and tokens used to authenticate against Microsoft Azure and other LLM services.

**Impact and Consequences**
- **Development Environment Compromise:** Developers using the compromised package may have had their local workstations and cloud-connected development environments fully exposed.
- **Pipeline Poisoning:** Automated build systems that automatically pull the latest version of LiteLLM could have been used to inject backdoors into production AI models or services.

**Recommended Actions**
- **I. Governance & Containment:** Immediately audit all projects for LiteLLM 1.107.0 and revert to a known-secure version (e.g., 1.106.x).
- **II. Identity & Access Management:** Rotate all credentials, API keys, and service principal secrets that were present in environments where the compromised package was installed.
- **III. Infrastructure Intelligence:** Implement software composition analysis (SCA) tools to block the installation of unverified or compromised package versions in CI/CD pipelines.
- **IV. Operational Resilience:** Isolate AI development environments from production secrets using Azure Key Vault with restricted access policies.
- **V. Simulation & Testing:** Conduct a threat hunt for unauthorized outbound network connections originating from Python-based development containers.

**Conclusion**
This incident underscores the fragility of the AI software supply chain and the necessity of strict dependency pinning and integrity verification for third-party libraries.

**Further Reading**
[1. Microsoft Security Blog: Inside the LiteLLM 1.107.0 supply chain compromise](https://www.microsoft.com/en-us/security/blog/2026/10/23/inside-the-litellm-1-107-0-supply-chain-compromise-credential-throw-through-python-startup-hooks/)

---

## Incident Title: Microsoft 365 Token-Replay Attacks Affecting 79 Organizations — Late September 2026

**Incident Metadata:**
- **Primary Category:** M365
- **Timeline:** Event: July 14 – September 22, 2026 | Disclosed: October 2026
- **Impacted Products:** Microsoft 365, Entra ID
- **Impacted Country:** Global
- **List of Companies Impacted:** 79 organizations

Cybersecurity researchers observed a widespread campaign leveraging Adversary-in-the-Middle (AitM) relay techniques to capture and replay Microsoft 365 session tokens, resulting in the compromise of 97 accounts across 79 organizations.

**Overview**
Between mid-July and late September 2026, threat actors successfully bypassed standard multi-factor authentication (MFA) by intercepting session cookies in real-time. By replaying these tokens, the attackers gained unauthorized access to corporate email accounts, bypassing the need for password or MFA re-authentication.

**Technical Details**
- **AitM Relay:** Attackers deployed phishing proxies that acted as a transparent bridge between the user and the legitimate Microsoft 365 login page, capturing the session token upon successful authentication.
- **Token Replay:** Once the session token was captured, it was imported into the attacker’s browser, allowing them to impersonate the victim and access M365 resources without triggering further security challenges.

**Impact and Consequences**
- **Business Email Compromise (BEC):** Unauthorized access to email accounts allowed attackers to conduct internal reconnaissance, launch further phishing campaigns, and intercept sensitive business communications.
- **Data Exfiltration:** Access to M365 environments provided a gateway to sensitive documents stored in SharePoint and OneDrive.

**Recommended Actions**
- **I. Governance & Containment:** Enforce Conditional Access policies that require compliant devices or FIDO2-based hardware security keys, which are resistant to AitM relay attacks.
- **II. Identity & Access Management:** Implement "Continuous Access Evaluation" (CAE) in Entra ID to revoke sessions immediately upon suspicious activity or location changes.
- **III. Infrastructure Intelligence:** Monitor Entra ID sign-in logs for anomalous "User Agent" strings or impossible travel patterns that indicate token replay.
- **IV. Operational Resilience:** Deploy phishing-resistant MFA across all user tiers.
- **V. Simulation & Testing:** Conduct regular phishing simulations that specifically test for AitM-style proxy attacks.

**Conclusion**
Traditional MFA is no longer sufficient against sophisticated AitM relay attacks; organizations must transition to phishing-resistant authentication methods.

**Further Reading**
[1. The Hacker News: Microsoft 365 Token-Replay Attacks](https://thehackernews.com/2026/10/microsoft-365-token-replay-attacks.html)

---

## Incident Title: BlackX UEFI Bootkit Targeting Diplomatic Entities — Early 2026

**Incident Metadata:**
- **Primary Category:** WINDOWS SERVER
- **Timeline:** Event: Early 2026 | Disclosed: October 2026
- **Impacted Products:** Windows (UEFI Secure Boot)
- **Impacted Country:** Tajikistan, Uzbekistan, Turkmenistan
- **List of Companies Impacted:** Diplomatic organizations

A sophisticated UEFI bootkit dubbed "BlackX," attributed to the China-linked actor APT41, has been identified bypassing Secure Boot on patched Windows systems by exploiting missing revocations in the firmware.

**Overview**
The BlackX bootkit represents a high-tier threat that operates at the firmware level, allowing it to persist across OS reinstalls and remain invisible to traditional kernel-mode security software. The attack specifically targeted diplomatic entities in Central Asia, demonstrating a high degree of geopolitical motivation.

**Technical Details**
- **Secure Boot Bypass:** The bootkit exploits vulnerabilities in the UEFI boot process, specifically targeting systems where the revocation lists (DBX) for vulnerable bootloaders have not been updated.
- **Persistence:** By infecting the UEFI firmware, the malware gains execution priority before the Windows kernel, effectively neutralizing OS-level security controls.

**Impact and Consequences**
- **Systemic Compromise:** Once the bootkit is installed, the integrity of the entire operating system is compromised, allowing for the installation of persistent backdoors and data exfiltration tools.
- **Undetectability:** Because the malware resides in the firmware, standard antivirus and EDR solutions are unable to detect or remove the infection.

**Recommended Actions**
- **I. Governance & Containment:** Ensure all hardware is updated with the latest UEFI firmware and that the Windows DBX (revocation list) is current.
- **II. Identity & Access Management:** Implement hardware-backed security (TPM 2.0) and Measured Boot to detect unauthorized changes to the boot chain.
- **III. Infrastructure Intelligence:** Utilize Microsoft Defender for Endpoint to monitor for firmware-level anomalies and unauthorized bootloader modifications.
- **IV. Operational Resilience:** Enforce strict physical access controls to prevent unauthorized firmware flashing.
- **V. Simulation & Testing:** Perform periodic integrity checks of the UEFI environment using specialized forensic tools.

**Conclusion**
Firmware-level attacks are becoming a preferred vector for state-sponsored actors; organizations must prioritize firmware hygiene as part of their core security strategy.

**Further Reading**
[1. The Hacker News: BlackX UEFI Bootkit](https://thehackernews.com/2026/10/blackx-uefi-bootkit-bypasses-secure.html)