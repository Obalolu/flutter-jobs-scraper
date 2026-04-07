#!/usr/bin/env python3
"""
Flutter Jobs Nigeria - Daily Job Scraper
Version: 1.0.0
Purpose: Search and match Flutter/Dart developer jobs for Oba
"""

import json
import re
from datetime import datetime
from pathlib import Path

# Configuration
OUTPUT_DIR = Path("/root/.openclaw/workspace/logs")
TODAY = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = OUTPUT_DIR / f"flutter-jobs-{TODAY}.md"

# Oba's CV Profile
OBA_SKILLS = {
    # Primary skills (weight: 10)
    "flutter": 10,
    "dart": 10,
    "riverpod": 10,
    "firebase": 10,
    "firestore": 10,
    "clean architecture": 10,
    
    # Secondary skills (weight: 7)
    "supabase": 7,
    "rest api": 7,
    "graphql": 5,
    "bloc": 7,
    "state management": 7,
    "payments": 7,
    "push notifications": 7,
    "ci/cd": 7,
    
    # Other skills (weight: 5)
    "kotlin": 5,
    "java": 5,
    "android": 5,
    "ios": 5,
    "git": 5,
    "jira": 5,
    "postman": 5,
    "clean code": 5,
    "agile": 5,
}

# Negative keywords (reduce confidence)
SENIOR_KEYWORDS = [
    "senior", "lead", "principal", "staff engineer", "head of",
    "5+ years", "7+ years", "8+ years", "10+ years",
    "architect", "team lead", "manager", "director"
]

JUNIOR_KEYWORDS = [
    "junior", "entry", "intern", "graduate", "trainee",
    "1-2 years", "1-3 years", "0-2 years", "fresher"
]

REMOTE_KEYWORDS = [
    "remote", "work from home", "wfh", " Telecommute", "hybrid"
]

NIGERIA_KEYWORDS = [
    "nigeria", "lagos", "abuja", "port harcourt", "kano", "ibadan", "ng"
]

# Job sources to search
SOURCES = [
    # Nigerian Job Boards
    {"name": "Indeed Nigeria", "url": "https://ng.indeed.com/Flutter-Developer-jobs", "search_param": ""},
    {"name": "MyJobMag", "url": "https://www.myjobmag.com/jobs-by-title/flutter-app-developer", "search_param": ""},
    {"name": "MyJobMag - Mobile Dev", "url": "https://www.myjobmag.com/jobs-by-title/mobile-developer-(flutter", "search_param": ""},
    {"name": "HotNigerianJobs", "url": "https://www.hotnigerianjobs.com/", "search_param": "flutter developer"},
    {"name": "Jobberman", "url": "https://www.jobberman.com/search?search=flutter+developer", "search_param": ""},
    {"name": "NigeriaJob.com", "url": "https://www.nigeriajob.com/", "search_param": "flutter"},
    {"name": "Jobberlad", "url": "https://jobberlad.com/", "search_param": "flutter"},
    
    # Tech/Flutter Specific
    {"name": "FlutterJobs", "url": "https://flutterjobs.com/africa/ng", "search_param": ""},
    {"name": "Glassdoor Lagos", "url": "https://www.glassdoor.com/Job/lagos-flutter-developer-jobs-SRCH_IL.0,5_IC2543876_KO6,23.htm", "search_param": ""},
    {"name": "Glassdoor Nigeria", "url": "https://www.glassdoor.com/Job/nigeria-mobile-developer-jobs-SRCH_IL.0,7_IN177_KO8,24.htm", "search_param": ""},
    
    # Remote Work (Nigeria)
    {"name": "RemoteAfrica", "url": "https://remoteafrica.io/", "search_param": "flutter"},
    {"name": "Indeed Remote", "url": "https://ng.indeed.com/q-flutter-developer,-remote-l-lagos-jobs.html", "search_param": ""},
    
    # LinkedIn
    {"name": "LinkedIn Nigeria", "url": "https://ng.linkedin.com/jobs/flutter-jobs", "search_param": ""},
]

# Search queries (rotated daily)
SEARCH_QUERIES = [
    "Flutter developer Nigeria junior 2026",
    "Flutter developer Lagos entry level 2026",
    "Mobile developer Flutter Nigeria intern 2026",
    "Junior Flutter developer remote Africa 2026",
    "Flutter Dart developer Lagos mid-level 2026",
    "Flutter developer job requirements Nigeria",
    "Mobile app developer Nigeria Flutter Firebase",
]

def calculate_confidence(job_title, job_description, company_name=""):
    """Calculate confidence score based on CV matching"""
    text = f"{job_title} {job_description} {company_name}".lower()
    
    score = 0
    max_score = 0
    matched_skills = []
    missing_skills = []
    
    # Check skills match
    for skill, weight in OBA_SKILLS.items():
        max_score += weight
        if skill in text:
            score += weight
            matched_skills.append(skill)
        elif "flutter" in text or "mobile" in text:
            # For mobile jobs, consider related skills
            missing_skills.append(skill)
    
    # Normalize to percentage
    if max_score > 0:
        confidence = min(100, int((score / max_score) * 100))
    else:
        confidence = 30
    
    # Senior penalty
    for keyword in SENIOR_KEYWORDS:
        if keyword in text:
            confidence -= 40
            break
    
    # Junior/Entry bonus
    for keyword in JUNIOR_KEYWORDS:
        if keyword in text:
            confidence += 15
            break
    
    # Remote bonus
    for keyword in REMOTE_KEYWORDS:
        if keyword in text:
            confidence += 10
            break
    
    # Nigeria bonus
    for keyword in NIGERIA_KEYWORDS:
        if keyword in text:
            confidence += 10
            break
    
    # Clamp confidence
    confidence = max(0, min(100, confidence))
    
    return confidence, matched_skills, missing_skills

def get_action_tier(confidence):
    """Determine action tier based on confidence"""
    if confidence >= 85:
        return "🔥 Apply Now"
    elif confidence >= 70:
        return "📞 DM Recruiter"
    elif confidence >= 50:
        return "📝 Save for Later"
    else:
        return "❌ Skip"

def categorize_confidence(confidence):
    """Categorize confidence level"""
    if confidence >= 85:
        return "HIGH"
    elif confidence >= 70:
        return "MEDIUM"
    elif confidence >= 50:
        return "LOW"
    else:
        return "POOR"

class Job:
    """Job listing data structure"""
    def __init__(self, title, company, location, url, description="", 
                 salary="", source="", experience="", level="",
                 skills_required=None, confidence=0, matched_skills=None):
        self.title = title
        self.company = company
        self.location = location
        self.url = url
        self.description = description
        self.salary = salary
        self.source = source
        self.experience = experience
        self.level = level
        self.skills_required = skills_required or []
        self.confidence = confidence
        self.matched_skills = matched_skills or []
    
    def to_dict(self):
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "url": self.url,
            "description": self.description,
            "salary": self.salary,
            "source": self.source,
            "experience": self.experience,
            "level": self.level,
            "skills_required": self.skills_required,
            "confidence": self.confidence,
            "matched_skills": self.matched_skills
        }

def format_job_card(jobs, title="Job Opportunities"):
    """Format jobs as markdown cards"""
    if not jobs:
        return "No jobs found matching criteria."
    
    output = []
    for i, job in enumerate(jobs, 1):
        tier = get_action_tier(job['confidence'])
        cat = categorize_confidence(job['confidence'])
        
        output.append(f"### {i}. {job['title']}")
        output.append(f"**{tier}** | {cat} Match ({job['confidence']}%)")
        output.append(f"- 🏢 Company: {job.get('company', 'N/A')}")
        output.append(f"- 📍 Location: {job.get('location', 'N/A')}")
        
        if job.get('salary'):
            output.append(f"- 💰 Salary: {job['salary']}")
        
        output.append(f"- 🔗 [Apply Here]({job['url']})")
        
        if job.get('source'):
            output.append(f"- 📱 Source: {job['source']}")
        
        if job['matched_skills']:
            output.append(f"- ✅ Matched: {', '.join(job['matched_skills'][:5])}")
        
        output.append("")
    
    return "\n".join(output)

def generate_report(jobs):
    """Generate the daily report"""
    # Sort by confidence
    sorted_jobs = sorted(jobs, key=lambda x: x['confidence'], reverse=True)
    
    # Categorize
    high = [j for j in sorted_jobs if j['confidence'] >= 85]
    medium = [j for j in sorted_jobs if 70 <= j['confidence'] < 85]
    low = [j for j in sorted_jobs if 50 <= j['confidence'] < 70]
    remote = [j for j in sorted_jobs if 'remote' in j.get('location', '').lower() or 'remote' in j.get('description', '').lower()]
    
    report = []
    report.append(f"# 📱 Flutter Jobs Nigeria - {TODAY}")
    report.append(f"🔍 Deep Search | {len(jobs)} opportunities found")
    report.append("")
    report.append("---")
    report.append("")
    
    # High Priority
    if high:
        report.append("## 🔥 HIGH PRIORITY (Apply Today)")
        report.append("")
        report.append(format_job_card(high, "High Priority"))
        report.append("")
    
    # Medium Priority
    if medium:
        report.append("## ✅ MEDIUM PRIORITY")
        report.append("")
        report.append(format_job_card(medium, "Medium Priority"))
        report.append("")
    
    # Low Priority
    if low:
        report.append("## 📝 OTHER OPPORTUNITIES")
        report.append("")
        report.append(format_job_card(low[:10], "Other Opportunities"))  # Limit to top 10
        report.append("")
    
    # Summary
    report.append("---")
    report.append("## 📊 SUMMARY")
    report.append(f"- Total Found: {len(jobs)}")
    report.append(f"- High Confidence (85%+): {len(high)}")
    report.append(f"- Medium Confidence (70-84%): {len(medium)}")
    report.append(f"- Remote Opportunities: {len(remote)}")
    report.append("")
    report.append(f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}_")
    
    return "\n".join(report)

def main():
    """Main function - placeholder for now"""
    print("Flutter Jobs Scraper v1.0.0")
    print(f"Date: {TODAY}")
    print("-" * 40)
    print("This is the core engine.")
    print("Web scraping will be implemented in v2.0")
    print("")
    print("To run a search, use: web_search with Flutter job queries")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # For now, just log that we ran
    print(f"\nLog file: {LOG_FILE}")

if __name__ == "__main__":
    main()
