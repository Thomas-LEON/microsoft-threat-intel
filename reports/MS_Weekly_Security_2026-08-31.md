# 🔷 Microsoft Security — Weekly Threat Intel Briefing
**Report Date:** 2026-08-31
**Coverage Period:** 2026-08-24 → 2026-08-31

**Weekly Threat Score:** N/A
(Auditable Metrics - Threat Capability: 8/10 | Event Frequency: 9/10 | Business Impact: 8/10)

---

## Incident Title: TerminalFix Campaign Deploys Reverse Tunnel via Windows Terminal/PowerShell (August 28, 2026)

**Incident Metadata:**
- **Primary Category:** M365
- **Timeline:** Event: August 28, 2026 | Disclosed: August 28, 2026
- **Impacted Products:** Windows Terminal, PowerShell, Microsoft 365
- **Impacted Country:** Global
- **List of Companies Impacted:** Unknown

Microsoft Threat Intelligence has identified a sophisticated evolution of the "ClickFix" social engineering technique, now dubbed "TerminalFix," which bypasses traditional browser-based lures to execute malicious commands directly within Windows Terminal or PowerShell.

**Overview**
The TerminalFix campaign utilizes deceptive CAPTCHA prompts to trick users into copying and executing obfuscated commands. Unlike previous iterations that targeted the Windows "Run" dialog, this variant specifically targets the command-line interface, facilitating DLL sideloading and the establishment of a persistent reverse tunnel to attacker-controlled infrastructure.

**Technical Details**
- **Command-Line Hijacking:** The attack leverages the user's trust in the command-line interface, prompting them to paste commands that appear to be legitimate system diagnostic or security verification scripts.
- **Reverse Tunneling:** Once executed, the payload establishes a reverse tunnel, allowing threat actors to bypass perimeter firewalls and maintain persistent, interactive access to the compromised host.
- **DLL Sideloading:** The malicious script facilitates the loading of unauthorized DLLs into legitimate system processes, effectively masking the attacker's presence from basic monitoring tools.

**Impact and Consequences**
- **Full System Compromise:** The ability to execute commands as the logged-in user allows for lateral movement and credential harvesting.
- **Evasion of Traditional Defenses:** By utilizing legitimate Windows tools (Living-off-the-Land), the attack circumvents signature-based detection mechanisms.

**Recommended Actions**
- **I. Governance & Containment:** Implement strict AppLocker or Windows Defender Application Control (WDAC) policies to restrict the execution of unauthorized scripts.
- **II. Identity & Access Management:** Enforce the Principle of Least Privilege (PoLP) to ensure users do not have administrative rights to execute arbitrary PowerShell commands.
- **III. Infrastructure Intelligence:** Monitor for anomalous child processes spawned by `wt.exe` or `powershell.exe` using Microsoft Defender for Endpoint.
- **IV. Operational Resilience:** Conduct user awareness training specifically targeting "copy-paste" social engineering lures.
- **V. Simulation & Testing:** Utilize Microsoft Security Copilot to simulate the execution of the identified TerminalFix command patterns to verify detection efficacy.

**Conclusion**
TerminalFix highlights the shift toward abusing native administrative tools to bypass security controls, necessitating a move toward behavioral-based detection rather than simple file-based analysis.

**Further Reading**
[1. https://www.microsoft.com/en-us/security/blog/2026/08/28/terminalfix-campaign-deploys-reverse-tunnel-through-multistage-intrusion/](https://www.microsoft.com/en-us/security/blog/2026/08/28/terminalfix-campaign-deploys-reverse-tunnel-through-multistage-intrusion/)

---

## Incident Title: AI Infrastructure Exploitation: LiteLLM Gateway and Credential Harvesting (August 26, 2026)

**Incident Metadata:**
- **Primary Category:** COPILOT
- **Timeline:** Event: August 26, 2026 | Disclosed: August 26, 2026
- **Impacted Products:** Azure AI Infrastructure, LiteLLM Gateways
- **Impacted Country:** Global
- **List of Companies Impacted:** Unknown

Microsoft Threat Intelligence has observed an increase in attacks targeting exposed AI infrastructure, specifically focusing on LiteLLM gateways used to manage LLM workloads, leading to credential harvesting and cryptomining.

**Overview**
As organizations rapidly deploy AI agents, the underlying infrastructure—often including third-party gateways like LiteLLM—has become a prime target. Attackers are scanning for misconfigured gateways to gain unauthorized access to API keys and compute resources.

**Technical Details**
- **Gateway Exploitation:** Attackers exploit unpatched or misconfigured LiteLLM gateways to gain unauthorized access to the underlying AI service configurations.
- **Credential Harvesting:** Once inside, actors extract stored API keys and service principal credentials, which are then used to pivot into broader Azure environments.
- **Persistence & Cryptomining:** Compromised compute resources are repurposed for unauthorized cryptomining, leading to significant operational costs and performance degradation.

**Impact and Consequences**
- **Data Exfiltration:** Access to AI gateways can expose sensitive prompts and data processed by the LLMs.
- **Financial Loss:** Unauthorized use of Azure compute resources results in unexpected billing and potential service throttling.

**Recommended Actions**
- **I. Governance & Containment:** Ensure all AI gateways are behind a Web Application Firewall (WAF) and require robust authentication.
- **II. Identity & Access Management:** Rotate all API keys associated with AI services and implement Managed Identities for Azure resources to eliminate hardcoded credentials.
- **III. Infrastructure Intelligence:** Enable Azure Monitor and Microsoft Defender for Cloud to alert on anomalous compute usage patterns.
- **IV. Operational Resilience:** Regularly audit AI infrastructure configurations against the Microsoft Cloud Adoption Framework.
- **V. Simulation & Testing:** Perform penetration testing on AI gateway endpoints to identify potential exposure points.

**Conclusion**
Securing the "AI control plane" is now as critical as securing the traditional network perimeter, as AI agents become highly privileged identities within the enterprise.

**Further Reading**
[1. https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/](https://www.microsoft.com/en-us/security/blog/2026/08/26/when-ai-infrastructure-becomes-target-securing-gateways-control-points/)

---

## Incident Title: Malicious Chrome and Edge Extensions Deploying ClickFix Lures (August 2026)

**Incident Metadata:**
- **Primary Category:** SUPPLY CHAIN
- **Timeline:** Event: August 2026 | Disclosed: August 2026
- **Impacted Products:** Microsoft Edge, Google Chrome
- **Impacted Country:** Global
- **List of Companies Impacted:** Unknown

A cluster of 19 browser extensions, including one for Microsoft Edge, has been identified as malicious, deploying a framework designed to steal cryptocurrency and sensitive browser data while injecting ClickFix lures.

**Overview**
These extensions were published over the last six months and utilized sophisticated obfuscation to evade store review processes. Once installed, they deployed modules that monitored browser activity and injected malicious prompts to facilitate further compromise.

**Technical Details**
- **Data Exfiltration:** The extensions utilized background scripts to scrape browser history, cookies, and cryptocurrency wallet secrets.
- **ClickFix Injection:** The extensions dynamically injected fake security alerts (ClickFix) into the user's browser, prompting them to perform actions that would lead to further malware installation.
- **Persistence:** The extensions maintained persistence by hooking into browser startup processes, ensuring they remained active across sessions.

**Impact and Consequences**
- **Credential Theft:** Users' session tokens and saved passwords were at risk of exfiltration.
- **Financial Theft:** Direct draining of cryptocurrency wallets linked to the browser.

**Recommended Actions**
- **I. Governance & Containment:** Implement browser extension management policies via Microsoft Intune to block unauthorized or unverified extensions.
- **II. Identity & Access Management:** Require re-authentication for sensitive M365 applications if browser-based compromise is suspected.
- **III. Infrastructure Intelligence:** Use Microsoft Defender for Endpoint to scan for known malicious extension signatures and block associated C2 traffic.
- **IV. Operational Resilience:** Educate users on the risks of installing third-party browser extensions.
- **V. Simulation & Testing:** Conduct periodic audits of installed browser extensions across the enterprise fleet.

**Conclusion**
Browser extensions represent a significant, often overlooked, supply chain risk that requires centralized management and strict policy enforcement.

**Further Reading**
[1. https://thehackernews.com/2026/08/19-chrome-and-edge-extensions-found.html](https://thehackernews.com/2026/08/19-chrome-and-edge-extensions-found.html)