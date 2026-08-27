# 🔷 Microsoft Security — Weekly Threat Intel Briefing
**Report Date:** 2026-08-27
**Coverage Period:** 2026-08-20 → 2026-08-27

**Weekly Threat Score:** 79/100
*(Auditable Metrics - Threat Capability: 7/10 | Event Frequency: 9/10 | Business Impact: 8/10)*

---

## Incident Title: NovaCookies AitM Phishing Campaign Targeting Microsoft 365 Disclosed on August 26, 2026

**Incident Metadata:**
- **Primary Category:** M365
- **Timeline:** Disclosed: August 26, 2026 | Active: Mid-to-Late August 2026
- **Impacted Products:** Microsoft 365, Microsoft Entra ID
- **Impacted Country:** Global (primarily United States)
- **List of Companies Impacted:** Unknown (targeted broadly across multiple sectors)

A newly identified Adversary-in-the-Middle (AitM) phishing toolkit named "NovaCookies" is actively targeting Microsoft 365 users to bypass multi-factor authentication (MFA) and hijack active sessions.¹ The campaign, disclosed on August 26, 2026, leverages legitimate DocuSign notifications to trick victims into authenticating through a proxy server.²

**Overview**
Security researchers at Island disclosed details of NovaCookies, a subscription-based Phishing-as-a-Service (PhaaS) platform retailing for approximately $320 per month.¹ The toolkit lowers the barrier to entry for cybercriminals, allowing them to orchestrate sophisticated AitM attacks that steal more than just static credentials. By abusing genuine DocuSign notification templates and infrastructure, the threat actors successfully bypass traditional secure email gateways (SEGs) to deliver malicious links that harvest active Microsoft 365 session cookies.²

**Technical Details**
The NovaCookies platform operates as a reverse-proxy system designed to intercept real-time authentication flows:
- **DocuSign Abuse:** Attackers send phishing emails that mimic legitimate DocuSign document signature requests, or abuse actual DocuSign API endpoints to send authentic notifications containing malicious redirect URLs.¹
- **AitM Reverse Proxy:** When a victim clicks the link, they are directed to a proxy server that mirrors the legitimate Microsoft Entra ID login portal in real-time.
- **Session Cookie Harvesting:** As the victim inputs their credentials and completes their multi-factor authentication (MFA) challenge, the proxy intercepts the resulting session cookies (OAuth tokens) and forwards them to the attacker, bypassing the need to know the victim's actual password or MFA secrets.²

**Impact and Consequences**
- **MFA Bypass:** Because the proxy captures the post-authentication session token, traditional MFA methods (such as SMS, TOTP, or push notifications) are rendered ineffective.
- **Persistent Account Takeover:** Attackers gain immediate, authenticated access to the victim's Microsoft 365 tenant, enabling downstream Business Email Compromise (BEC), data exfiltration, and lateral movement.

**Recommended Actions**
To mitigate the risks exposed by this incident:
- **I. Governance & Containment (Prevention):** Implement strict email authentication protocols (SPF, DKIM, DMARC) and configure secure email gateways to flag external emails containing DocuSign links that redirect to unrecognized domains.
- **II. Identity & Access Management (Containment):** Transition high-risk and administrative users to phishing-resistant MFA standards, such as FIDO2 security keys or Windows Hello for Business, which cryptographically bind the authentication process to the legitimate domain.
- **III. Infrastructure Intelligence (Detection):** Create detection rules in Microsoft Sentinel to flag anomalous Entra ID sign-in logs, specifically looking for "impossible travel" alerts, unexpected user-agent strings, or session access from known proxy/VPN ranges.
- **IV. Operational Resilience:** Establish automated playbooks to immediately revoke active Microsoft 365 user sessions (`Revoke-MgUserSignInSession` via Microsoft Graph PowerShell) when suspicious AitM activity is detected.
- **V. Simulation & Testing:** Conduct targeted phishing simulations that mimic AitM proxy attacks to educate employees on verifying the browser address bar during authentication flows.

**Conclusion**
The commercialization of toolkits like NovaCookies demonstrates that standard MFA is no longer sufficient to protect enterprise identities. Organizations must prioritize the adoption of phishing-resistant authentication to defend against proxy-based session hijacking.

**Further Reading**
- [The Hacker News: NovaCookies Campaigns Abuse Genuine DocuSign Notifications](https://thehackernews.com/2026/08/novacookies-campaigns-abuse-genuine.html)

**Footnotes**
[1] https://thehackernews.com/2026/08/novacookies-campaigns-abuse-genuine.html  
[2] https://www.darkreading.com/endpoint-security/novacookies-steals-microsoft-365-sessions-320-a-month

---

## Incident Title: Mirage2FA Phishing-as-a-Service Campaign Targeting Microsoft 365 Disclosed on August 26, 2026

**Incident Metadata:**
- **Primary Category:** M365
- **Timeline:** Disclosed: August 26, 2026 | Active: 2024 to August 2026
- **Impacted Products:** Microsoft 365, Microsoft Entra ID
- **Impacted Country:** United States, European Union
- **List of Companies Impacted:** Over 4,500 companies targeted

A massive commercial phishing campaign dubbed "Mirage2FA" has targeted thousands of organizations globally, abusing legitimate Microsoft 365 login flows to bypass two-factor authentication.¹ The campaign, analyzed and disclosed on August 26, 2026, has resulted in a high compromise rate among targeted enterprise accounts.

**Overview**
According to threat research published by ANY.RUN, the Mirage2FA campaign has actively targeted over 4,500 companies, primarily based in the United States and the European Union.¹ The campaign utilizes a highly sophisticated Phishing-as-a-Service (PhaaS) toolkit designed specifically to target Microsoft 365 accounts. By abusing legitimate Microsoft login flows, the toolkit has achieved a potential compromise rate of 48% among targeted email addresses, making it one of the most successful active identity-harvesting operations of the year.

**Technical Details**
The Mirage2FA toolkit relies on dynamic reverse-proxy infrastructure to manipulate the authentication process:
- **Login Flow Abuse:** The phishing kit dynamically communicates with the legitimate Microsoft Entra ID identity provider, presenting the victim with a real-time replica of the Microsoft login interface.¹
- **MFA Interception:** When the victim enters their credentials and receives an MFA prompt (such as a push notification or a one-time passcode), the proxy captures the response and relays it to Microsoft's servers.
- **Token Extraction:** Once authenticated, the proxy extracts the session token (cookie) and saves it for the attacker, allowing them to maintain persistent access without triggering subsequent security alerts.

**Impact and Consequences**
- **Systemic Tenant Compromise:** With a 48% compromise rate, organizations face a high probability of tenant intrusion, leading to unauthorized access to SharePoint, OneDrive, and Exchange Online.
- **Downstream Phishing and BEC:** Attackers leverage compromised accounts to send highly convincing internal phishing emails to other employees, partners, and vendors, expanding the attack surface.

**Recommended Actions**
To mitigate the risks exposed by this incident:
- **I. Governance & Containment (Prevention):** Enforce tenant restriction policies in Microsoft Entra ID to prevent users from authenticating against external, unauthorized tenants.
- **II. Identity & Access Management (Containment):** Implement Microsoft Entra ID Conditional Access policies that mandate Phishing-Resistant MFA (such as FIDO2 keys) for all enterprise users, especially those in finance, HR, and IT.
- **III. Infrastructure Intelligence (Detection):** Monitor Entra ID sign-in logs for anomalous device properties, such as unexpected operating system and browser combinations, or logins originating from hosting provider IP ranges.
- **IV. Operational Resilience:** Configure Entra ID Protection to automatically block or force a password reset/session revocation for users flagged with "High" sign-in risk.
- **V. Simulation & Testing:** Run red-team exercises simulating proxy-based MFA bypasses to evaluate the detection capabilities of your Security Operations Center (SOC).

**Conclusion**
The scale and efficiency of the Mirage2FA campaign highlight the limitations of traditional, non-phishing-resistant MFA. Organizations must adapt by implementing strict conditional access controls and monitoring for anomalous session behavior.

**Further Reading**
- [The Hacker News: Mirage2FA Surge Hits 4,500 US and EU Companies](https://thehackernews.com/2026/08/mirage2fa-surge-hits-4500-us-and-eu.html)

**Footnotes**
[1] https://thehackernews.com/2026/08/mirage2fa-surge-hits-4500-us-and-eu.html

---

## Incident Title: Doubloon Dredger Campaign Abusing Notion to Harvest Microsoft 365 Authentication Tokens Disclosed on August 27, 2026

**Incident Metadata:**
- **Primary Category:** SUPPLY CHAIN
- **Timeline:** Disclosed: August 27, 2026 | Active: Late August 2026
- **Impacted Products:** Microsoft 365, Microsoft Entra ID, Notion
- **Impacted Country:** Global
- **List of Companies Impacted:** Unknown

A novel cyberespionage and credential harvesting campaign named "Doubloon Dredger" has been observed abusing Notion's collaborative platform to steal Microsoft 365 authentication tokens.¹ The campaign, disclosed on August 27, 2026, bypasses traditional secure email gateways by hosting malicious landing pages on legitimate SaaS infrastructure.

**Overview**
The Doubloon Dredger campaign represents a sophisticated supply chain and platform abuse attack. Threat actors distribute malicious PDF documents containing links that direct victims to legitimate Notion pages (`notion.so`).¹ Because Notion is a highly trusted enterprise collaboration tool, these links easily bypass standard URL reputation filters. Once on the Notion page, victims are prompted to interact with elements that initiate malicious OAuth application consent flows or redirect them to AitM login portals designed to harvest Microsoft Entra ID authentication tokens.

**Technical Details**
The campaign exploits trust relationships between SaaS platforms and Microsoft Entra ID:
- **SaaS Reputation Abuse:** Attackers host phishing content on legitimate Notion workspaces, ensuring that the initial delivery mechanism (email containing a Notion link) is classified as safe by secure email gateways.¹
- **OAuth Consent Phishing:** The Notion pages often direct users to grant permissions to a malicious, attacker-controlled Azure/Entra ID enterprise application.
- **Token Harvesting:** Once the victim grants consent, the malicious application receives an OAuth authorization code, which the attacker exchanges for access and refresh tokens, granting them persistent access to the victim's M365 data.

**Impact and Consequences**
- **Bypass of Perimeter Defenses:** Traditional secure email gateways and web content filters fail to block the initial phishing vectors due to the use of legitimate Notion domains.
- **Persistent, Passwordless Access:** By securing OAuth tokens, attackers maintain persistent access to the victim's mailbox and files without needing to know their password or bypass MFA on subsequent connections.

**Recommended Actions**
To mitigate the risks exposed by this incident:
- **I. Governance & Containment (Prevention):** Configure Microsoft Entra ID user consent settings to restrict users from consenting to multi-tenant applications from unverified publishers without administrator approval.
- **II. Identity & Access Management (Containment):** Regularly audit enterprise applications and consented permissions within the Entra ID portal, revoking any unrecognized or high-privilege third-party integrations.
- **III. Infrastructure Intelligence (Detection):** Monitor Entra ID audit logs for events related to new service principal creation, consent grants (`Consent to application`), and anomalous API calls via Microsoft Graph.
- **IV. Operational Resilience:** Implement automated alerts in Microsoft Defender for Cloud Apps to flag when a user grants high-risk permissions (e.g., `Mail.Read`, `Files.ReadWrite.All`) to an external application.
- **V. Simulation & Testing:** Conduct security awareness training specifically focusing on the risks of OAuth consent phishing and the importance of verifying application permissions.

**Conclusion**
The Doubloon Dredger campaign underscores the growing trend of threat actors abusing trusted SaaS ecosystems to target Microsoft enterprise identities. Restricting user-led OAuth consent is a critical control for preventing persistent, passwordless tenant compromise.

**Further Reading**
- [InfoSecurity Magazine: Doubloon Dredger Abuses Notion to Harvest Authentication Tokens](https://www.infosecurity-magazine.com/news/doubloon-dredger-notion/)

**Footnotes**
[1] https://www.infosecurity-magazine.com/news/doubloon-dredger-notion/

---

## Incident Title: CISA Adds Microsoft SQL Server Remote Code Execution Vulnerability (CVE-2019-1068) to KEV Catalog on August 26, 2026

**Incident Metadata:**
- **Primary Category:** CVE
- **Timeline:** Added to KEV: August 26, 2026 | Disclosed: July 9, 2019
- **Impacted Products:** Microsoft SQL Server 2014, Microsoft SQL Server 2016, Microsoft SQL Server 2017
- **Impacted Country:** Global
- **List of Companies Impacted:** Unknown (targeted broadly in the wild)

The Cybersecurity and Infrastructure Security Agency (CISA) has added a critical legacy Microsoft SQL Server remote code execution vulnerability, CVE-2019-1068, to its Known Exploited Vulnerabilities (KEV) catalog.¹ The addition, made on August 26, 2026, follows recent evidence of active exploitation targeting unpatched database servers in the wild.²

**Overview**
On August 26, 2026, CISA updated its KEV catalog to include CVE-2019-1068, a high-severity remote code execution (RCE) vulnerability affecting multiple legacy versions of Microsoft SQL Server.¹ Although Microsoft patched this vulnerability in July 2019, threat actors continue to actively scan for and exploit unpatched, internet-facing, or poorly segmented SQL Server instances within enterprise networks to execute arbitrary code and establish initial access.²

**Technical Details**
The vulnerability stems from an out-of-bounds memory write flaw within the database engine:
- **Vulnerability Mechanism:** The flaw exists in the way the Microsoft SQL Server Database Engine handles internal memory pointers during the execution of specific database queries.¹
- **Exploitation Vector:** An authenticated attacker with low-privilege database access can execute a specially crafted SQL query that triggers an out-of-bounds memory write, leading to remote code execution under the security context of the SQL Server service account.
- **Post-Exploitation:** Once code execution is achieved, attackers typically attempt to escalate privileges to the local system level, harvest credentials, and move laterally across the internal network.

**Impact and Consequences**
- **Full Host Compromise:** Successful exploitation allows attackers to run arbitrary commands on the database host, potentially leading to complete control of the underlying operating system.
- **Data Exfiltration and Ransomware:** Because SQL Servers host sensitive corporate data, compromised instances are highly vulnerable to data theft, database encryption, and ransomware deployment.

**Recommended Actions**
To mitigate the risks exposed by this incident:
- **I. Governance & Containment (Prevention):** Immediately inventory all Microsoft SQL Server deployments within the enterprise, identifying legacy versions (2014, 2016, 2017) that may have missed historical patch cycles.
- **II. Identity & Access Management (Containment):** Enforce the principle of least privilege by restricting database service account permissions and ensuring SQL Server ports (default TCP 1433) are not exposed to the public internet.
- **III. Infrastructure Intelligence (Detection):** Deploy intrusion detection system (IDS) signatures to monitor for anomalous SQL queries and configure endpoint detection and response (EDR) tools to flag unexpected child processes spawned by `sqlservr.exe`.
- **IV. Operational Resilience:** Apply the official Microsoft security updates for CVE-2019-1068 immediately to all affected SQL Server instances.
- **V. Simulation & Testing:** Perform regular vulnerability scanning and penetration testing targeting database infrastructure to ensure legacy systems are not left unpatched.

**Conclusion**
The active exploitation of a 2019 SQL Server vulnerability in 2026 serves as a stark reminder that legacy systems and delayed patch cycles remain a primary entry point for enterprise network intrusions. Organizations must ensure that legacy database environments are strictly segmented and fully patched.

**Further Reading**
- [The Hacker News: CISA Adds Six Exploited Flaws to KEV](https://thehackernews.com/2026/08/cisa-adds-six-exploited-flaws-to-kev.html)

**Footnotes**
[1] https://thehackernews.com/2026/08/cisa-adds-six-exploited-flaws-to-kev.html  
[2] https://www.infosecurity-magazine.com/news/cisa-kev-microsoft-citrix/