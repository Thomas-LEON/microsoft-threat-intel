# 🔷 Microsoft Security — Weekly Threat Intel Briefing
**Report Date:** 2026-09-24
**Coverage Period:** 2026-09-17 → 2026-09-24

**Weekly Threat Score:** N/A
(Auditable Metrics - Threat Capability: 9/10 | Event Frequency: 9/10 | Business Impact: 8/10)

---

## Incident Title: Microsoft Disrupts EvilTokens Phishing-as-a-Service (PaaS) Infrastructure — September 22, 2026

**Incident Metadata:**
- **Primary Category:** M365
- **Timeline:** Event: September 22, 2026 | Disclosed: September 22, 2026
- **Impacted Products:** Microsoft 365, Entra ID
- **Impacted Country:** Global
- **List of Companies Impacted:** Unknown (12,000+ accounts compromised)

Microsoft, in coordination with the U.S. District Court for the Eastern District of Virginia and industry partners, successfully disrupted the "EvilTokens" PhaaS platform, which utilized AI-assisted lures and device code phishing to compromise over 12,000 Microsoft 365 accounts.¹ ²

**Overview**
EvilTokens operated as a sophisticated PhaaS platform that automated the entire attack chain, from generating AI-assisted phishing lures to managing the infrastructure required for device code phishing. By tricking users into entering device codes, attackers bypassed traditional MFA, allowing them to steal session tokens. Microsoft’s Digital Crimes Unit (DCU) seized 50 websites and disabled over 150 domains associated with the service.

**Technical Details**
- **Device Code Phishing:** The platform exploited the OAuth 2.0 Device Authorization Grant flow, which is designed for input-constrained devices but is frequently abused to bypass MFA by tricking users into authorizing a malicious application.
- **AI-Driven Automation:** The platform integrated AI at every stage, including the generation of highly convincing phishing lures and the automated management of C2 infrastructure to rotate domains and evade detection.

**Impact and Consequences**
- **Credential Theft:** Over 12,000 enterprise accounts were compromised, leading to potential data exfiltration and lateral movement within affected M365 tenants.
- **MFA Bypass:** The technique effectively rendered standard MFA ineffective, as the user was tricked into granting the attacker a valid session token.

**Recommended Actions**
- **I. Governance & Containment:** Disable the "Device Code" flow for users who do not require it via Entra ID Conditional Access policies.
- **II. Identity & Access Management:** Enforce phishing-resistant MFA (FIDO2/Passkeys) to mitigate the risk of token theft.
- **III. Infrastructure Intelligence:** Monitor Entra ID sign-in logs for anomalous device code authentication patterns.
- **IV. Operational Resilience:** Conduct regular user awareness training specifically focused on the dangers of entering device codes from untrusted sources.
- **V. Simulation & Testing:** Use Microsoft’s Attack Simulation Training to test user susceptibility to device code phishing lures.

**Conclusion**
The disruption of EvilTokens highlights the shift toward AI-automated phishing. Organizations must move beyond legacy MFA and adopt phishing-resistant authentication to defend against modern session-theft techniques.

**Further Reading**
[1. Microsoft Security Blog: Unmasking EvilTokens](https://www.microsoft.com/en-us/security/blog/2026/09/22/unmasking-eviltokens-getting-to-the-root-of-device-code-phishing/)
[2. The Hacker News: Microsoft Takes Down EvilTokens](https://thehackernews.com/2026/09/microsoft-takes-down-eviltokens-device.html)

---

## Incident Title: SharePoint Server Vulnerability CVE-2026-65660 Escalated to Authenticated RCE — September 23, 2026

**Incident Metadata:**
- **Primary Category:** CVE
- **Timeline:** Event: September 23, 2026 | Disclosed: September 23, 2026
- **Impacted Products:** SharePoint Server 2016, 2019, Subscription Edition
- **Impacted Country:** Global
- **List of Companies Impacted:** Unknown

A SharePoint Server vulnerability, initially categorized by Microsoft as a low-severity spoofing flaw, has been confirmed by security researchers to allow for authenticated Remote Code Execution (RCE).¹

**Overview**
The vulnerability, tracked as CVE-2026-65660, was originally misclassified as a spoofing issue with a CVSS score of 6.5. New technical analysis by Viettel Cyber Security researcher Dinh Ho Anh Khoa demonstrates that an authenticated attacker can leverage this flaw to execute arbitrary code on the underlying server.

**Technical Details**
- **Misclassification Risk:** The initial assessment failed to account for the full exploit chain, which allows an attacker with sufficient privileges to bypass security controls and achieve RCE.
- **Exploit Vector:** The flaw affects the core processing logic of SharePoint Server 2016, 2019, and the Subscription Edition, requiring an attacker to have authenticated access to the environment.

**Impact and Consequences**
- **System Compromise:** Successful exploitation grants the attacker full control over the SharePoint server, potentially leading to data theft, lateral movement, and persistence within the corporate network.
- **Security Trust:** The misclassification highlights the importance of independent security research in verifying vendor-provided severity ratings.

**Recommended Actions**
- **I. Governance & Containment:** Immediately audit all SharePoint environments for the latest security patches.
- **II. Identity & Access Management:** Restrict administrative access to SharePoint to the absolute minimum number of users.
- **III. Infrastructure Intelligence:** Deploy EDR solutions on SharePoint servers to detect suspicious child processes spawned by the web server service.
- **IV. Operational Resilience:** Ensure a robust backup and recovery plan is in place for all SharePoint content databases.
- **V. Simulation & Testing:** Perform internal penetration testing to verify that SharePoint patches are correctly applied and effective.

**Conclusion**
This incident serves as a reminder that vendor severity ratings should be treated as a baseline, not a final assessment. Organizations must prioritize patching based on the potential for RCE, regardless of initial classification.

**Further Reading**
[1. The Hacker News: SharePoint Flaw Initially Listed as Spoofing Enables Authenticated RCE](https://thehackernews.com/2026/09/sharepoint-flaw-initially-listed-as.html)

---

## Incident Title: Chinese Threat Actor UTA0565 Exploits Chrome-Windows Zero-Day Chain — September 23, 2026

**Incident Metadata:**
- **Primary Category:** WINDOWS SERVER
- **Timeline:** Event: September 03–04, 2026 | Disclosed: September 23, 2026
- **Impacted Products:** Windows (Advanced Local Procedure Call), Google Chrome
- **Impacted Country:** Global
- **List of Companies Impacted:** Unknown

A Chinese threat actor, identified as UTA0565, was observed exploiting a zero-day chain involving Google Chrome and the Windows Advanced Local Procedure Call (ALPC) to deploy the CLEANGULP malware.¹ ²

**Overview**
Detected in early September 2026, the attack chain utilized two Chrome vulnerabilities (CVE-2026-85046, CVE-2026-87491) and one Windows ALPC vulnerability (CVE-2026-85880). The attackers used fake websites to lure victims into the exploit chain, which ultimately allowed for sandbox escape and code execution on the host Windows system.

**Technical Details**
- **Exploit Chaining:** The attack demonstrates a high level of sophistication by chaining browser-based vulnerabilities with a Windows kernel-level (ALPC) flaw to achieve full system compromise.
- **CLEANGULP Malware:** The payload, CLEANGULP, is designed for stealthy persistence and data exfiltration, characteristic of state-sponsored espionage campaigns.

**Impact and Consequences**
- **System Compromise:** The ability to escape the browser sandbox and execute code on the Windows host provides attackers with significant control over the endpoint.
- **Espionage Risk:** The use of zero-day chains suggests a highly capable adversary focused on long-term intelligence gathering.

**Recommended Actions**
- **I. Governance & Containment:** Ensure all browsers and Windows systems are updated to the latest versions to mitigate known exploit chains.
- **II. Identity & Access Management:** Implement strict application control (e.g., AppLocker or Windows Defender Application Control) to prevent unauthorized execution.
- **III. Infrastructure Intelligence:** Monitor for unusual ALPC activity and unexpected network connections from browser processes.
- **IV. Operational Resilience:** Maintain offline backups of critical data to ensure recovery in the event of a ransomware or wiper-style attack.
- **V. Simulation & Testing:** Conduct threat hunting exercises focused on identifying indicators of compromise (IoCs) associated with known Chinese threat groups.

**Conclusion**
The use of zero-day chains targeting both browser and OS components remains a primary threat vector for sophisticated actors. Defense-in-depth, including robust endpoint protection and rapid patching, is essential.

**Further Reading**
[1. CyberScoop: Volexity spots another China-aligned threat group](https://cyberscoop.com/volexity-uta0565-china-exploit-chain-chrome-microsoft/)
[2. The Hacker News: Chinese Hackers Exploit Chrome-Windows Zero-Day Chain](https://thehackernews.com/2026/09/chinese-hackers-exploit-chrome-windows.html)