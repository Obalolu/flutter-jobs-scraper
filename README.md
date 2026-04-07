# Flutter Jobs Nigeria Scraper

An automated job search tool that finds Flutter and mobile developer opportunities in Nigeria (and remote options) and matches them against your CV skills.

---

## What It Does

- Searches multiple Nigerian job boards daily for Flutter developer jobs
- Matches job requirements against your skills to give a confidence score
- Categorizes jobs by priority (Apply Now, DM Recruiter, Save for Later)
- Provides direct apply links for each opportunity
- Runs automatically every day at 9:00 AM Nigeria time

---

## Job Sources

- Indeed Nigeria
- MyJobMag
- Glassdoor
- Jobberlad
- RemoteAfrica
- LinkedIn
- Company career pages (Flutterwave, Andela, Paystack, etc.)
- Remote job platforms (Turing, Wellfound, Working Nomads)

---

## Current Opportunities

14 active job listings as of today, including:
- Lagos-based positions (ByteWorks, Zojatech, TEZDA, etc.)
- Remote positions (Andela, RemoteAfrica, Turing, etc.)
- Major tech companies (Flutterwave, Paystack, Moniepoint)

---

## How to Use

1. Check the latest jobs in `logs/flutter-jobs-YYYY-MM-DD.md`
2. Look at the confidence score to gauge how well you match
3. Click the apply link to submit your application

---

## Project Structure

```
flutter-jobs-scraper/
├── scripts/
│   ├── flutter-jobs-scraper.py   # Core matching engine
│   ├── flutter-jobs-daily.sh     # Daily runner
│   └── flutter-jobs-daemon.sh    # Background daemon
├── logs/
│   └── flutter-jobs-*.md         # Daily job listings
├── cv-analysis.md                # CV skills analysis
└── README.md
```

---

## Daily Workflow

1. Every morning at 9:00 AM (Nigeria time), the scraper runs
2. Searches for new Flutter/mobile developer jobs
3. Scores each job based on your skills
4. Updates the job listings with new opportunities
5. Creates a PR with improvements

---

## Skills Matched

Your CV is matched against these key skills:

- Flutter, Dart, Riverpod, BLoC
- Firebase, Firestore, Supabase
- Clean Architecture
- REST APIs, Payments
- Push Notifications

---

## Contributing

This is a personal job search automation tool. Feel free to fork and adapt for your own job search.

---

Last updated: 2026-04-07