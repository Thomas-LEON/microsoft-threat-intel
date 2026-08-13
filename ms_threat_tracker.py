import os
import datetime
import feedparser
import re
import httpx
from google import genai
from google.genai import types
from bs4 import BeautifulSoup

# ============================================================================
# Microsoft Threat Intel — Weekly Security Tracker
# ============================================================================
# Automated pipeline that scrapes cybersecurity RSS feeds, filters them through
# Gemini AI with strict Microsoft-ecosystem focus, and generates a structured
# executive-ready Markdown report twice a week (Monday + Thursday).
# ============================================================================

API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")

# ---------------------
# RSS Feed Sources
# ---------------------
# Mix of Microsoft-specific feeds and top general cybersecurity feeds.
# The AI prompt handles the Microsoft-focus filtering for general feeds.

RSS_FEEDS = [
    # --- Microsoft Official Feeds ---
    "https://msrc.microsoft.com/blog/feed",                             # MSRC Blog (official vulnerability disclosures)
    "https://www.microsoft.com/en-us/security/blog/feed/",              # Microsoft Security Blog
    "https://azure.microsoft.com/en-us/blog/feed/",                     # Azure Blog (includes security updates)
    "https://techcommunity.microsoft.com/feeds/blog/Microsoft365Blog",  # M365 Blog (TechCommunity)
    "https://techcommunity.microsoft.com/feeds/blog/MicrosoftEntraBlog",# Entra ID Blog (TechCommunity)

    # --- General Cybersecurity Feeds (filtered by AI for Microsoft relevance) ---
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://www.darkreading.com/rss.xml",
    "https://www.cyberscoop.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.securityweek.com/feed/",
    "https://www.infosecurity-magazine.com/rss/news/",
    "https://techcrunch.com/category/security/feed/",
    "https://feeds.arstechnica.com/arstechnica/security",
]

# ---------------------
# Microsoft keyword pre-filter for general feeds (performance optimization)
# Articles from Microsoft-specific feeds are always kept.
# Articles from general feeds must mention at least one Microsoft keyword.
# ---------------------
MICROSOFT_KEYWORDS = [
    "microsoft", "azure", "m365", "office 365", "office365",
    "copilot", "entra", "defender", "intune", "sharepoint",
    "outlook", "exchange", "teams", "onedrive", "power platform",
    "power automate", "power bi", "powerbi", "power apps",
    "windows server", "active directory", "ad fs", "adfs",
    "msrc", "patch tuesday", "ms patch", "cve-", "kb5",
    "github copilot", "security copilot", "bing chat",
    "dynamics 365", "dynamics365", "sql server",
    "azure devops", "visual studio", "vscode", "vs code",
    ".net", "dotnet", "asp.net", "nuget",
    "hyper-v", "hyperv", "windows 11", "windows 10",
    "edge browser", "microsoft edge",
]

MICROSOFT_FEED_DOMAINS = [
    "msrc.microsoft.com",
    "microsoft.com",
    "azure.microsoft.com",
    "techcommunity.microsoft.com",
]


def is_microsoft_feed(feed_url: str) -> bool:
    """Check if a feed URL belongs to a Microsoft-official source."""
    return any(domain in feed_url for domain in MICROSOFT_FEED_DOMAINS)


def contains_microsoft_keyword(text: str) -> bool:
    """Check if text contains at least one Microsoft-related keyword."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in MICROSOFT_KEYWORDS)


def fetch_recent_news():
    """Fetch articles published in the last 7 days from all RSS feeds.

    Microsoft-official feeds: all articles are kept.
    General feeds: only articles mentioning Microsoft keywords are kept.
    """
    recent_articles = []
    now = datetime.datetime.now(datetime.timezone.utc)
    one_week_ago = now - datetime.timedelta(days=7)

    for feed_url in RSS_FEEDS:
        ms_feed = is_microsoft_feed(feed_url)
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime.datetime(
                        *entry.published_parsed[:6], tzinfo=datetime.timezone.utc
                    )
                    if published > one_week_ago:
                        title = entry.title or ""
                        summary = entry.get("summary", "")

                        # Microsoft feeds: keep everything. General feeds: keyword filter.
                        if ms_feed or contains_microsoft_keyword(title + " " + summary):
                            recent_articles.append({
                                "title": title,
                                "link": entry.link,
                                "summary": summary,
                                "source": feed.feed.get("title", feed_url),
                            })
        except Exception as e:
            print(f"Error reading feed {feed_url}: {e}")

    return recent_articles


def get_previously_covered_incidents(weeks=2):
    """Retrieve incident titles from the last N weekly reports to avoid duplicates.

    Looks back at both Monday and Thursday reports for the specified number of weeks.
    """
    covered = []
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    if not os.path.exists(output_dir):
        return covered

    now = datetime.datetime.now()
    for i in range(1, (weeks * 7) + 1):
        target_date = (now - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        filepath = os.path.join(output_dir, f"MS_Weekly_Security_{target_date}.md")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                titles = re.findall(r"^## (.*)", content, re.MULTILINE)
                for t in titles:
                    clean_t = t.strip()
                    if clean_t:
                        covered.append(clean_t)
    return list(set(covered))


def generate_executive_summary(articles, covered_incidents=None):
    """Use Gemini AI to filter articles and generate a Microsoft-focused executive report."""
    if not articles:
        return "No major Microsoft security incidents or vulnerabilities detected in the past 7 days."

    try:
        client = genai.Client(
            api_key=API_KEY,
            http_options={"httpx_client": httpx.Client(verify=False)},
        )

        prompt = """
        You are a senior cybersecurity analyst specializing in the Microsoft ecosystem.
        Your role is to identify and analyze security incidents, vulnerabilities, and emerging risks
        SPECIFICALLY related to Microsoft products, platforms, and services.

        Below is a list of articles collected over the past 7 days. Your mission is to identify a
        TOP 1 to 15 of the most significant Microsoft-related security items, and write a detailed,
        structured report for EACH of them.

        === STRICT INCLUSION CRITERIA (article MUST match at least one) ===
        1. **Microsoft Platform Vulnerabilities**: CVEs, zero-days, or security flaws in Azure, M365,
           Windows Server, Exchange, SharePoint, Teams, Entra ID (Azure AD), Intune, Defender,
           Power Platform, SQL Server, .NET, ASP.NET, Dynamics 365.
        2. **Microsoft Copilot & AI Security**: Prompt injection, data leakage, misconfiguration, or
           abuse of MS Copilot (M365 Copilot, GitHub Copilot, Security Copilot), AI integrations,
           plugin/connector risks, Copilot Studio vulnerabilities.
        3. **Azure Cloud Security**: Misconfigurations, breaches, identity attacks (Entra ID/Azure AD),
           storage exposure, Azure DevOps, Azure Kubernetes Service (AKS), Azure Functions,
           Azure OpenAI Service incidents.
        4. **Microsoft Supply Chain & Ecosystem**: Attacks leveraging Microsoft's ecosystem (OAuth app
           consent phishing, malicious Azure Marketplace apps, compromised NuGet/npm packages for MS
           tech stacks, Microsoft-signed driver abuse).
        5. **Patch Tuesday & Security Advisories**: Monthly patch details, actively exploited
           vulnerabilities, emergency out-of-band patches, MSRC advisories.
        6. **M365 & Productivity Suite Threats**: Business Email Compromise (BEC) via Outlook/Exchange,
           SharePoint/OneDrive data exposure, Teams-based phishing, malicious Power Automate flows.
        7. **Microsoft Infrastructure Attacks**: Attacks ON Microsoft itself (corporate breaches,
           Midnight Blizzard/Nobelium campaigns, source code leaks, internal system compromises).

        === STRICT EXCLUSION CRITERIA (MUST ignore) ===
        1. Incidents with NO connection to Microsoft products, services, or platforms.
        2. Generic ransomware/phishing campaigns not specifically exploiting Microsoft technology.
        3. Consumer-grade Windows issues (home edition gaming bugs, Xbox, personal Outlook.com spam).
        4. Old/recycled news — verify that each event occurred WITHIN the last 7 days.
        5. Pure product announcements, feature launches, or marketing content with no security angle.

        === THREAT SCORE EVALUATION (CRQ / FAIR METHODOLOGY) ===
        BEFORE listing the first incident, you MUST evaluate the overall weekly severity based on the
        most critical incident. Score these 3 vectors from 1 to 10:
        1. Threat Capability (TC): Sophistication of the attack (1 = Script kiddie, 10 = Nation-State Zero Day).
        2. Event Frequency (EF): Likelihood of exploitation targeting Microsoft enterprise customers (1 = Very low, 10 = Imminent/Active).
        3. Business Impact (BI): Financial, systemic, and reputational impact (1 = Negligible, 10 = Critical/Systemic).

        Leave the final mathematical calculation to the Python code. You MUST provide the scores in
        THIS EXACT FORMAT as the very first line of your report:
        *(Auditable Metrics - Threat Capability: X/10 | Event Frequency: Y/10 | Business Impact: Z/10)*

        Then skip a line and begin listing incidents.

        === REPORT STRUCTURE (MANDATORY for each incident) ===
        Separate each incident with a horizontal rule (---).

        ## Incident Title: Must INCLUDE the Microsoft products/services affected and the most precise date

        **Incident Metadata:**
        - **Primary Category:** [One keyword: AZURE, M365, COPILOT, CVE, ENTRA ID, SUPPLY CHAIN, EXCHANGE, TEAMS, WINDOWS SERVER, DEFENDER, POWER PLATFORM, etc.]
        - **Timeline:** [Event: most precise date | Disclosed: most precise disclosure date]
        - **Impacted Products:** [Specific Microsoft products/services affected]
        - **Impacted Country:** [Country impacted, or "Global" / "Unknown"]
        - **List of Companies Impacted:** [Companies affected, if known]

        [Short 1-2 sentence introduction addressing the problem. EXPLICITLY name the Microsoft products and the precise date.]

        **Overview**
        [One paragraph summarizing the situation, naming actors, exact dates, and Microsoft infrastructure details]

        **Technical Details**
        [Contextual explanation of the mechanism]
        - [Point 1: **Bold title** and explanation]
        - [Point 2: **Bold title** and explanation]
        - ...

        **Impact and Consequences**
        - [Impact 1: **Bold title** and explanation]
        - [Impact 2: **Bold title** and explanation]
        - ...

        **Recommended Actions**
        To mitigate the risks exposed by this incident:
        - **I. Governance & Containment (Prevention):** [Proposed action]
        - **II. Identity & Access Management (Containment):** [Proposed action]
        - **III. Infrastructure Intelligence (Detection):** [Proposed action]
        - **IV. Operational Resilience:** [Proposed action]
        - **V. Simulation & Testing:** [Proposed action]
        (Tailor each control to the specific nature of the Microsoft threat!)

        **Conclusion**
        [Short conclusion on the lesson learned from this incident]

        **Further Reading**
        [Additional relevant link(s) if available]

        **Footnotes**
        [1. Source link 1]
        [2. Source link 2]

        Write the entire report in English. Use a highly professional, executive, analytical, and concise tone.
        Use footnotes (superscript indices like: ¹ ²) in the text to link to the Footnotes section of each incident.
        Remember to separate each incident with '---'.

        Here are the raw articles:
        """

        for i, art in enumerate(articles):
            soup = BeautifulSoup(art["summary"], "html.parser")
            clean_summary = soup.get_text()[:400]
            prompt += (
                f"\n- Title: {art['title']}\n"
                f"  Link: {art['link']}\n"
                f"  Source: {art['source']}\n"
                f"  Excerpt: {clean_summary}\n"
            )

        if covered_incidents:
            prompt += "\n\nABSOLUTE EXCLUSION CRITERION (ALREADY COVERED DUPLICATES):\n"
            prompt += (
                "The following incidents have ALREADY been covered in our previous reports. "
                "You MUST NOT include them in this report (some RSS feeds resurface old articles). "
                "Ignore them completely:\n"
            )
            for ci in covered_incidents:
                prompt += f"- {ci}\n"

        models_to_try = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.1-flash-lite"]

        for model_name in models_to_try:
            try:
                print(f"Attempting generation with model {model_name}...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.2),
                )
                return response.text
            except Exception as e:
                print(f"Failed with model {model_name}: {e}")
                continue

        return "Error: Unable to generate report with available Gemini models (3.6, 3.5, 3.1-lite)."

    except Exception as e:
        return (
            f"Error calling the AI API: {e}\n"
            "Have you configured the GEMINI_API_KEY environment variable?"
        )


def main():
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    week_start = (
        datetime.datetime.now() - datetime.timedelta(days=7)
    ).strftime("%Y-%m-%d")

    print(f"=== Microsoft Security Weekly Tracker ===")
    print(f"Coverage period: {week_start} to {today_str}")
    print()

    print("Fetching Microsoft-related security news from the past 7 days...")
    articles = fetch_recent_news()
    print(f"{len(articles)} Microsoft-relevant articles found.")

    print("Checking previous reports to avoid duplicates...")
    covered = get_previously_covered_incidents(weeks=2)
    if covered:
        print(f"  → {len(covered)} previously covered incident(s) will be excluded.")

    print("AI analysis and executive report generation in progress...")
    report = generate_executive_summary(articles, covered_incidents=covered)

    # --- Deterministic Threat Score Calculation ---
    print("Computing deterministic risk score (CRQ/FAIR)...")
    match = re.search(
        r"\*\(\s*Auditable Metrics\s*-\s*Threat Capability:\s*(\d+)/10\s*\|\s*"
        r"Event Frequency:\s*(\d+)/10\s*\|\s*Business Impact:\s*(\d+)/10\s*\)\*",
        report,
        re.IGNORECASE,
    )

    if match:
        tc = int(match.group(1))
        ef = int(match.group(2))
        bi = int(match.group(3))
        threat_score = int((tc + ef + bi) * 3.33)
        threat_score = min(threat_score, 100)

        report = report.replace(
            match.group(0),
            f"**Weekly Threat Score:** {threat_score}/100\n{match.group(0)}",
        )
    else:
        report = "**Weekly Threat Score:** N/A\n" + report

    # --- Save Report ---
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"MS_Weekly_Security_{today_str}.md")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# 🔷 Microsoft Security — Weekly Threat Intel Briefing\n")
        f.write(f"**Report Date:** {today_str}\n")
        f.write(f"**Coverage Period:** {week_start} → {today_str}\n\n")
        f.write(report)

    print(f"\nDone! Report saved to:\n{filename}")


if __name__ == "__main__":
    main()
