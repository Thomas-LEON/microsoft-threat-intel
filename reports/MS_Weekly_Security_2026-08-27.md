# 🔷 Microsoft Security — Weekly Threat Intel Briefing
**Report Date:** 2026-08-27
**Coverage Period:** 2026-08-20 → 2026-08-27

**Weekly Threat Score:** 79/100
*(Auditable Metrics - Threat Capability: 7/10 | Event Frequency: 9/10 | Business Impact: 8/10)*

---

## Incident Title: NovaCookies Phishing Kit Abuses DocuSign Notifications to Hijack Microsoft 365 Enterprise Sessions (Late August 2026)

**Incident Metadata:**
- **Primary Category:** M365
- **Timeline:** Event: Late August 2026 | Disclosed: August 21, 2026
- **Impacted Products:** Microsoft 365, Entra ID, Outlook
- **Impacted Country:** Global
- **List of Companies Impacted:** Enterprise Microsoft 365 tenants (specific corporate names undisclosed)

On August 21, 2026, cybersecurity researchers disclosed details regarding NovaCookies, an Adversary-in-the-Middle (AitM) phishing platform abusing legitimate DocuSign notification workflows to hijack Microsoft 365 authenticated sessions.

**Overview**
Disclosed on August 21, 2026, by researchers at cybersecurity firm Island, NovaCookies operates as a commercial Phishing-as-a-Service (PhaaS) platform available for $320 per month.¹ The campaign leverages genuine DocuSign infrastructure and routing to send initial notification emails to corporate targets, bypassing traditional Secure Email Gateways (SEGs). Victims who interact with the notification are directed through reverse-proxy landing pages that mirror live Microsoft 365 login endpoints (`login.microsoftonline.com`). This enables threat actors to seamlessly intercept credentials, multi-factor authentication (MFA) prompts, and post-authentication session cookies.

**Technical Details**
The technical mechanism relies on real-time proxying of Microsoft 365 identity provider (IdP) traffic:
- **DocuSign Infrastructure Abuse:** Threat actors register rogue accounts or abuse legitimate DocuSign notification features to dispatch real, cryptographic-signed emails containing malicious reverse-proxy redirection URLs.
- **Reverse-Proxy Session Interception:** The NovaCookies proxy intercepts the HTTP request/response pipeline between the victim's browser and Microsoft Entra ID authentication endpoints.
- **Session Cookie and Token Harvesting:** Upon the target completing password and MFA entry, NovaCookies captures essential session cookies (`ESTSAUTH` and `ESTSAUTHPERSISTENT`) along with OAuth tokens, enabling persistent tenant access without alerting the user.

**Impact and Consequences**
- **Multi-Factor Authentication Bypass:** Circumvents standard SMS, TOTP authenticator app, and push notification MFA mechanisms by stealing active post-MFA authorization cookies.
- **Enterprise Account Takeover:** Provides threat actors with full, persistent access to Microsoft 365 applications, including Exchange Online, Teams, SharePoint, and OneDrive, facilitating downstream Business Email Compromise (BEC) and corporate espionage.

**Recommended Actions**
To mitigate the risks exposed by this incident:
- **I. Governance & Containment (Prevention):** Establish strict mail flow rules to inspect incoming e-signature notification links and restrict user access to unauthorized reverse-proxy landing domains.
- **II. Identity & Access Management (Containment):** Enforce Microsoft Entra ID Conditional Access policies mandating compliant, Microsoft Intune-managed, or Microsoft Entra hybrid joined devices for all session requests.
- **III. Infrastructure Intelligence (Detection):** Configure Microsoft Defender for Identity and Entra ID Risk Logs to alert on anomalous session cookie usage originating from non-standard IP ranges or unrecognized device footprints.
- **IV. Operational Resilience:** Accelerate the adoption of FIDO2 hardware security keys or WebAuthn passwordless authentication, which cryptographically bind the user login to the genuine origin URL (`login.microsoftonline.com`).
- **V. Simulation & Testing:** Conduct advanced AitM phishing simulations across corporate Microsoft 365 tenants to assess user awareness against reverse-proxy social engineering lures.

**Conclusion**
The emergence of NovaCookies underscores the evolving threat landscape where cybercriminals exploit trusted enterprise communication platforms (DocuSign) and reverse-proxy frameworks to bypass Microsoft 365 MFA defenses. Organizations must shift toward context-aware and device-bound identity controls to effectively thwart session hijacking.

**Further Reading**
- [Dark Reading: NovaCookies Kit Steals Microsoft 365 Sessions for $320 a Month](https://www.darkreading.com/endpoint-security/novacookies-steals-microsoft-365-sessions-320-a-month)

**Footnotes**
¹ https://thehackernews.com/2026/08/novacookies-campaigns-abuse-genuine.html
² https://www.darkreading.com/endpoint-security/novacookies-steals-microsoft-365-sessions-320-a-month

---

## Incident Title: Mirage2FA Commercial Toolkit Abuses Microsoft 365 Login Flows Across 4,500 Enterprises (Late August 2026)

**Incident Metadata:**
- **Primary Category:** M365
- **Timeline:** Event: Late August 2026 | Disclosed: Late August 2026
- **Impacted Products:** Microsoft 365, Entra ID
- **Impacted Country:** United States, European Union, Global
- **List of Companies Impacted:** Over 4,500 enterprise organizations in the US and EU

In late August 2026, security researchers revealed a massive surge in the Mirage2FA phishing-as-a-service campaign, which compromised Microsoft 365 session flows across more than 4,500 enterprise tenants in the US and EU.

**Overview**
Research published in late August 2026 by ANY.RUN detailed a broad escalation of the Mirage2FA Phishing-as-a-Service (PhaaS) platform targeting Microsoft 365 enterprise environments.¹ Active across 2024–2026 and experiencing a massive expansion in August 2026, the toolkit has hit over 4,500 corporate organizations—predominantly located in the United States and Europe. Analysis reveals that approximately 48% of the targeted Microsoft 365 accounts were potentially compromised through dynamic Adversary-in-the-Middle (AitM) techniques that hijack active enterprise login sessions.

**Technical Details**
Mirage2FA functions as a high-throughput, automated credential and token harvesting platform:
- **Dynamic M365 Flow Proxying:** The tool automatically customizes landing pages using real-time organization branding pulled directly from Microsoft Entra ID based on the victim's email domain.
- **Real-Time MFA Relay:** The proxy relays authentication traffic live to official Microsoft endpoints, intercepting user passwords, TOTP codes, and push notification tokens as they are entered.
- **Token Exfiltration Infrastructure:** Once authentication succeeds, the backend extracts the resulting session state and token response, writing session cookies to attacker-controlled C2 servers while forwarding the victim to legitimate Microsoft 365 portals.

**Impact and Consequences**
- **High Enterprise Compromise Rate:** Achieving an approximate 48% compromise rate among targeted M365 email accounts, posing significant risk to enterprise perimeter defenses.
- **Mass Exposure of Cloud Workspaces:** Hijacked sessions yield full access to cloud assets hosted on Exchange Online, Microsoft OneDrive, Teams, and SharePoint, exposing proprietary enterprise data.

**Recommended Actions**
To mitigate the risks exposed by this incident:
- **I. Governance & Containment (Prevention):** Establish strict location-based and IP-reputation Conditional Access controls in Microsoft Entra ID to block sign-in attempts from unauthorized regions.
- **II. Identity & Access Management (Containment):** Enforce Certificate-Based Authentication (CBA) or FIDO2-based authentication mechanisms that resist AitM relay attacks.
- **III. Infrastructure Intelligence (Detection):** Enable Microsoft Defender for Cloud Apps to detect "Impossible Travel" and anomalous concurrent session activity across Microsoft 365 tenants.
- **IV. Operational Resilience:** Implement automated revocation playbooks via Microsoft Graph API to revoke active refresh tokens and terminate open browser sessions upon identity risk alerts.
- **V. Simulation & Testing:** Perform red-team simulations focusing on real-time AitM authentication flows to evaluate enterprise security monitoring response times.

**Conclusion**
The widespread impact of the Mirage2FA campaign highlights the scale and efficiency of commercialized AitM platforms targeting Microsoft 365. Relying solely on legacy MFA (such as SMS or app notifications) is no longer sufficient to guarantee identity security against modern proxy-based phishing frameworks.

**Further Reading**
- [ANY.RUN Security Research on Mirage2FA Phishing Campaign](https://thehackernews.com/2026/08/mirage2fa-surge-hits-4500-us-and-eu.html)

**Footnotes**
¹ https://thehackernews.com/2026/08/mirage2fa-surge-hits-4500-us-and-eu.html

---

## Incident Title: CISA Adds Active Microsoft SQL Server Remote Code Execution Vulnerability (CVE-2019-1068) to KEV Catalog (Late August 2026)

**Incident Metadata:**
- **Primary Category:** WINDOWS SERVER
- **Timeline:** Event: Late August 2026 | Disclosed: August 21, 2026
- **Impacted Products:** Microsoft SQL Server 2012, SQL Server 2014, SQL Server 2016, SQL Server 2017
- **Impacted Country:** Global
- **List of Companies Impacted:** Unidentified Federal Agencies and Commercial Infrastructure deploying legacy SQL Server engines

On August 21, 2026, the U.S. Cybersecurity and Infrastructure Security Agency (CISA) added a legacy Microsoft SQL Server Remote Code Execution flaw (CVE-2019-1068) to its Known Exploited Vulnerabilities (KEV) catalog following evidence of active exploitation.

**Overview**
On August 21, 2026, CISA issued a binding security update adding CVE-2019-1068 to its Known Exploited Vulnerabilities catalog.¹ CVE-2019-1068 is a high-severity Remote Code Execution (RCE) flaw present in several supported and extended versions of Microsoft SQL Server (2012 through 2017). Although originally addressed by Microsoft in a 2019 security bulletin, recent threat intelligence confirms that threat actors are actively exploiting unpatched, internet-exposed, or internally accessible SQL Server instances to execute arbitrary code with elevated database permissions.

**Technical Details**
The security vulnerability exists within the memory handling of the Microsoft SQL Server Database Engine:
- **Incorrect Pointer Handling:** The flaw stems from improper handling of specific pointers within the SQL Server database engine when executing crafted database queries or stored procedures.
- **Authenticated Code Execution:** An authenticated attacker with low-privilege database access can craft malicious SQL queries to trigger memory corruption and execute arbitrary code in the security context of the SQL Server Database Engine Service Account (`NT Service\MSSQLSERVER`).
- **Domain Pivot Potential:** If the SQL service account operates with local administrator or Domain Admin privileges, successful code execution allows attackers to compromise the underlying Windows Server OS and pivot laterally into the Active Directory environment.

**Impact and Consequences**
- **Full Infrastructure Takeover:** Remote code execution on critical enterprise database host servers.
- **Unauthorized Data Access:** Complete exposure, alteration, or deletion of sensitive databases hosted on compromised Microsoft SQL Server instances.

**Recommended Actions**
To mitigate the risks exposed by this incident:
- **I. Governance & Containment (Prevention):** Immediately verify and deploy Microsoft Security Update KB4505218 / KB4505219 across all legacy Microsoft SQL Server installations.
- **II. Identity & Access Management (Containment):** Enforce strict Principle of Least Privilege (PoLP) configuration on SQL Server accounts and ensure the SQL Server Service Account runs under a low-privileged Managed Service Account (gMSA).
- **III. Infrastructure Intelligence (Detection):** Enable Microsoft Defender for SQL and monitor Windows Event logs for unusual child processes spawned by `sqlservr.exe` (e.g., `cmd.exe` or `powershell.exe`).
- **IV. Operational Resilience:** Restrict inbound network access to SQL Server ports (default TCP 1433) using network security groups and host-based Windows Defender Firewalls.
- **V. Simulation & Testing:** Utilize Microsoft Defender Vulnerability Management to perform comprehensive asset discovery and identify unpatched SQL Server instances across corporate networks.

**Conclusion**
The addition of CVE-2019-1068 to CISA's KEV catalog serves as a critical reminder that legacy vulnerabilities in foundational Microsoft infrastructure remain prime targets for exploitation if patch cycles are neglected.

**Further Reading**
- [CISA Known Exploited Vulnerabilities Catalog](https://thehackernews.com/2026/08/cisa-adds-six-exploited-flaws-to-kev.html)

**Footnotes**
¹ https://thehackernews.com/2026/08/cisa-adds-six-exploited-flaws-to-kev.html

---

## Incident Title: Doubloon Dredger Threat Campaign Abuses Notion and Malicious PDFs to Harvest Microsoft Authentication Tokens (Late August 2026)

**Incident Metadata:**
- **Primary Category:** SUPPLY CHAIN
- **Timeline:** Event: Late August 2026 | Disclosed: Late August 2026
- **Impacted Products:** Microsoft 365, Microsoft Entra ID Authentication Tokens
- **Impacted Country:** Global
- **List of Companies Impacted:** Enterprise users relying on Microsoft 365 and external cloud workspace services

In late August 2026, security analysts discovered a new cyber campaign named Doubloon Dredger that weaponizes Notion pages and malicious PDFs to extract Microsoft Entra ID authentication tokens from enterprise targets.

**Overview**
Disclosed in late August 2026, the threat activity group tracked as Doubloon Dredger was observed using high-reputation workspace platforms—specifically Notion—alongside embedded PDF redirect chains to systematically capture Microsoft authentication tokens.¹ By hosting phishing lures on trusted cloud platforms like Notion (`notion.site`), the attackers circumvent static reputation checks built into email protection systems. Once users engage with the lures, they are led through specialized redirect chains that request Microsoft 365 consent or prompt for credentials, ultimately exfiltrating active Entra ID OAuth tokens.

**Technical Details**
The campaign employs a multi-tiered lure and token extraction architecture:
- **Reputation Abusing Lures:** The attackers host interactive documents on Notion and distribute malicious PDF attachments containing hyperlinked buttons to bypass domain reputation filters.
- **Redirect Chain Routing:** Clicks are routed through dynamic redirection layers that evaluate user-agent strings and environment signatures to evade automated sandbox detection.
- **OAuth & Session Token Extraction:** The campaign forces authentication requests that harvest Microsoft Entra ID access tokens, refresh tokens, and authentication cookies, granting persistent API access without necessitating password re-entry.

**Impact and Consequences**
- **Persistent Cloud Workspace Access:** Captured Entra ID refresh tokens allow continuous API access to Microsoft 365 cloud resources (Outlook, OneDrive, Graph API) without triggering traditional MFA challenges.
- **Evasion of Mail Protection Gateways:** The abuse of trusted subdomains (e.g., Notion) severely impairs the efficacy of perimeter secure email gateways.

**Recommended Actions**
To mitigate the risks exposed by this incident:
- **I. Governance & Containment (Prevention):** Restrict user consent settings within Microsoft Entra ID to prohibit end-users from granting access to unverified enterprise OAuth applications.
- **II. Identity & Access Management (Containment):** Implement Continuous Access Evaluation (CAE) and shorten Microsoft Entra ID refresh token lifetimes to minimize the window of opportunity for stolen tokens.
- **III. Infrastructure Intelligence (Detection):** Configure Microsoft Defender for Office 365 to analyze links inside external document attachments and cloud collaboration shares.
- **IV. Operational Resilience:** Enforce Microsoft Defender for Cloud Apps Conditional Access App Control to block token-based access from unmanaged or non-compliant corporate endpoints.
- **V. Simulation & Testing:** Conduct threat hunting exercises using Kusto Query Language (KQL) in Microsoft Sentinel to detect anomalous token usage patterns and unusual OAuth app registrations.

**Conclusion**
Doubloon Dredger highlights a growing trend among cyber threat actors leveraging legitimate third-party SaaS platforms to stage attacks against Microsoft 365 enterprise tenants. Identity boundaries must be fortified with strict consent policies and continuous authentication checks.

**Further Reading**
- [Infosecurity Magazine: Doubloon Dredger Abuses Notion to Harvest Authentication Tokens](https://www.infosecurity-magazine.com/news/doubloon-dredger-notion/)

**Footnotes**
¹ https://www.infosecurity-magazine.com/news/doubloon-dredger-notion/