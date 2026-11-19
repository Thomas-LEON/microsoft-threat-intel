# 🔷 Microsoft Security — Weekly Threat Intel Briefing
**Report Date:** 2026-11-19
**Coverage Period:** 2026-11-12 → 2026-11-19

**Weekly Threat Score:** 89/100
(Auditable Metrics - Threat Capability: 9/10 | Event Frequency: 9/10 | Business Impact: 9/10)

---

## Incident Title: Compromise of Microsoft’s Official Agent Framework PyPI Package — November 17, 2026

**Incident Metadata:**
- **Primary Category:** SUPPLY CHAIN
- **Timeline:** Event: November 17, 2026 | Disclosed: November 17, 2026
- **Impacted Products:** Microsoft Agent Framework (Python package), Azure, Azure DevOps, GitHub Actions
- **Impacted Country:** Global
- **List of Companies Impacted:** Developers and organizations utilizing the Microsoft Agent Framework

Threat actors successfully compromised the official Microsoft `agent-framework` package on the Python Package Index (PyPI), injecting malicious code into versions 1.26.1 and 1.26.2 to facilitate credential theft.

**Overview**
On November 17, 2026, security researchers identified that the official Microsoft `agent-framework` package on PyPI had been tampered with. Two malicious versions were published within a 33-minute window. These versions contained a payload designed to execute a credential stealer immediately upon the initialization of the Python environment, specifically targeting sensitive tokens for Azure, Azure DevOps, and GitHub Actions.

**Technical Details**
- **Credential Harvesting Mechanism:** The malicious code is designed to hook into the Python startup process, ensuring that the credential-stealing routine runs automatically whenever the library is imported.
- **Targeted Ecosystems:** The malware specifically scans for and exfiltrates environment variables and configuration files associated with Microsoft’s cloud and CI/CD infrastructure, effectively turning the developer's local machine into a pivot point for cloud environment compromise.

**Impact and Consequences**
- **Cloud Environment Exposure:** Successful exfiltration of Azure and GitHub Actions credentials grants attackers the ability to move laterally into production cloud environments, potentially leading to data breaches or unauthorized infrastructure modifications.
- **Supply Chain Contamination:** Organizations that automatically pull the latest versions of dependencies in their build pipelines may have inadvertently integrated the malicious code into their own software delivery lifecycle.

**Recommended Actions**
To mitigate the risks exposed by this incident:
- **I. Governance & Containment:** Immediately audit all CI/CD pipelines to identify if versions 1.26.1 or 1.26.2 of `agent-framework` were pulled. Pin dependencies to known-good versions using hash verification.
- **II. Identity & Access Management:** Revoke and rotate all Azure, Azure DevOps, and GitHub Actions credentials that were present on developer machines where the malicious package was installed.
- **III. Infrastructure Intelligence:** Deploy EDR/XDR solutions to monitor for anomalous Python process behavior and unauthorized outbound connections to known C2 infrastructure.
- **IV. Operational Resilience:** Implement a private package repository (e.g., Azure Artifacts) to proxy and scan external dependencies before they are available to internal developers.
- **V. Simulation & Testing:** Conduct a threat hunt for unauthorized access logs in Azure Entra ID associated with the compromised developer accounts.

**Conclusion**
This incident underscores the critical vulnerability of the software supply chain, where even trusted, official packages can be weaponized. It highlights the necessity of rigorous dependency management and the "assume breach" mindset for developer workstations.

**Further Reading**
[1. BleepingComputer: Microsoft's Agent Framework PyPI package compromised](https://www.bleepingcomputer.com/news/security/microsofts-agent-framework-pypi-package-compromised-to-steal-credentials/)
[2. The Hacker News: Attackers Compromise Microsoft's Agent Framework PyPI Package](https://thehackernews.com/2026/11/attackers-compromise-microsofts-agent.html)

---

## Incident Title: Operation ShadowCloud: GitDoor and GraphDoor Backdoors Leveraging SharePoint and GitHub — Early November 2026

**Incident Metadata:**
- **Primary Category:** M365
- **Timeline:** Event: Early November 2026 | Disclosed: November 17, 2026
- **Impacted Products:** Microsoft SharePoint, GitHub
- **Impacted Country:** Asia and Africa
- **List of Companies Impacted:** Government sectors (Undisclosed)

A sophisticated cyber-espionage campaign, dubbed "Operation ShadowCloud," has been identified utilizing legitimate Microsoft SharePoint and GitHub infrastructure as covert Command-and-Control (C2) channels.

**Overview**
Disclosed by Kaspersky in mid-November 2026, Operation ShadowCloud targets government entities in Asia and Africa. The attackers deployed two previously undocumented backdoors, GitDoor and GraphDoor, which bypass traditional network security controls by blending malicious traffic with legitimate API calls to Microsoft SharePoint and GitHub.

**Technical Details**
- **Covert C2 Channels:** The backdoors use the APIs of SharePoint and GitHub to exchange commands and exfiltrate data, making the malicious traffic appear as standard business communication.
- **Persistence Mechanism:** By leveraging trusted cloud services, the malware evades detection by network firewalls that typically allow traffic to these domains, complicating the identification of the C2 heartbeat.

**Impact and Consequences**
- **Data Exfiltration:** Sensitive government data is being funneled through trusted cloud platforms, making detection extremely difficult for standard security operations centers (SOCs).
- **Evasion of Perimeter Defense:** Because the traffic is directed toward legitimate Microsoft and GitHub endpoints, traditional IP-based blocking is ineffective.

**Recommended Actions**
To mitigate the risks exposed by this incident:
- **I. Governance & Containment:** Implement strict Conditional Access policies in Entra ID to restrict access to SharePoint and GitHub to managed, compliant devices only.
- **II. Identity & Access Management:** Monitor for unusual API usage patterns within SharePoint and GitHub, particularly for service accounts or automated scripts.
- **III. Infrastructure Intelligence:** Utilize Microsoft Defender for Cloud Apps to perform deep packet inspection and behavioral analysis on traffic directed toward SaaS applications.
- **IV. Operational Resilience:** Enforce strict egress filtering that inspects the content of API requests to cloud services rather than just the destination domain.
- **V. Simulation & Testing:** Conduct red team exercises simulating "living-off-the-cloud" techniques to test the SOC's ability to detect anomalous API activity.

**Conclusion**
Operation ShadowCloud demonstrates the evolving sophistication of threat actors who are increasingly "living off the cloud." Relying on domain reputation is no longer sufficient; security teams must focus on behavioral analysis of cloud service interactions.

**Further Reading**
[1. The Hacker News: New GitDoor and GraphDoor Backdoors Turn GitHub and SharePoint Into Covert C2 Channels](https://thehackernews.com/2026/11/new-gitdoor-and-graphdoor-backdoors.html)