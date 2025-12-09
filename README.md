# Gigography Scraper

A Python-based web scraper and Bash API client for extracting concert attendance data (gigography) from Songkick.

## 📊 Code Analysis

This repository has been comprehensively analyzed. View the detailed reports:

| Document | Description | Size |
|----------|-------------|------|
| [ANALYSIS_SUMMARY.md](ANALYSIS_SUMMARY.md) | Executive summary with scores and key findings | 4.9KB |
| [CODE_ANALYSIS.md](CODE_ANALYSIS.md) | Detailed Python script analysis | 8.2KB |
| [SHELL_SCRIPT_ANALYSIS.md](SHELL_SCRIPT_ANALYSIS.md) | Bash script analysis with security concerns | 6.0KB |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture and data flow | 7.8KB |

### Quick Scores

- **Python Script (songkick.py)**: ⭐⭐⭐⭐☆ (4/5)
- **Bash Script (songkick.sh)**: ⭐⭐☆☆☆ (2/5)
- **Overall Repository Health**: 6.5/10

## 🚀 Quick Start

### Python Web Scraper

**Dependencies:**
```bash
pip install requests beautifulsoup4
```

**Usage:**
```bash
python songkick.py
```

**Output:** Creates `songkick_gigography.csv` with columns: Date, Event Name, Venue, Location

### Bash API Client

**Prerequisites:**
- curl installed
- Songkick API key

**Usage:**
```bash
export SONGKICK_API_KEY='your_api_key_here'
./songkick.sh
```

**Output:** Creates XML files `0.xml` through `10.xml`

## 📁 Repository Structure

```
gigography/
├── songkick.py              # Main Python scraper (107 lines)
├── songkick.sh              # Bash API client (6 lines)
├── songkick_gigography.csv  # Output CSV file
├── *.xml                    # API response files
├── *.html                   # Cached HTML pages
├── *.json                   # Intermediate data
└── docs/
    ├── ANALYSIS_SUMMARY.md
    ├── CODE_ANALYSIS.md
    ├── SHELL_SCRIPT_ANALYSIS.md
    └── ARCHITECTURE.md
```

## 🔍 Key Features

### Python Scraper (songkick.py)
- ✅ Extracts data from JSON-LD structured data
- ✅ Automatic pagination with duplicate detection
- ✅ Rate limiting (1.5s between requests)
- ✅ CSV export with UTF-8 encoding
- ✅ Error handling for HTTP errors
- ⚠️ No request timeout (see recommendations)
- ⚠️ No logging infrastructure

### Bash Script (songkick.sh)
- ✅ Simple API data download
- ✅ Downloads pages 0-10
- ❌ API key exposed in URL (security issue)
- ❌ No error checking
- ❌ Limited flexibility

## 🔒 Security Considerations

### Python Script
- **Security Score**: 7/10
- Safe file handling with context managers
- No code execution vulnerabilities
- **Recommended**: Add request timeout, validate filename paths

### Bash Script
- **Security Score**: 4/10
- ⚠️ **HIGH RISK**: API key visible in process list and logs due to `-G` flag
- ⚠️ No HTTPS certificate verification
- **Recommended**: Use POST method without `-G` flag if API supports it

## 📝 Top Recommendations

### Immediate (High Priority)
1. Add `timeout=30` to Python requests.get()
2. Implement proper logging in Python (replace print statements)
3. Fix bash script API key exposure or document the risk
4. Add error checking to bash script

### Soon (Medium Priority)
5. Add command-line argument parsing to Python script
6. Create requirements.txt file
7. Add maximum page limit safety check
8. Validate filename to prevent path traversal

### Later (Low Priority)
9. Add comprehensive docstrings
10. Create unit tests
11. Improve type hints throughout
12. Add progress bar (e.g., tqdm)

## 🏗️ Architecture

The Python scraper uses a straightforward pipeline:

```
HTTP Request → HTML Parse → JSON-LD Extract → Duplicate Filter → CSV Export
```

- **Parser**: BeautifulSoup4
- **Data Source**: JSON-LD structured data (more reliable than CSS selectors)
- **Deduplication**: Set-based with composite key: `date|event_name|venue`
- **Output**: CSV with UTF-8 encoding

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed diagrams and flow charts.

## 📈 Performance

- **Memory Usage**: O(n) where n = number of unique gigs
- **Network Requests**: ~0.67 req/sec (rate limited)
- **Pagination**: Automatic stop when no new data found

## 🧪 Testing

Currently, no tests exist. See [CODE_ANALYSIS.md](CODE_ANALYSIS.md) for testing recommendations.

## 📖 Documentation

Each analysis document provides:
- **ANALYSIS_SUMMARY.md**: Quick overview, perfect for stakeholders
- **CODE_ANALYSIS.md**: Deep technical analysis for developers
- **SHELL_SCRIPT_ANALYSIS.md**: Bash script review with improved version
- **ARCHITECTURE.md**: System design and data flow diagrams

## 🤝 Contributing

Before making changes, please review:
1. Code analysis documents to understand current issues
2. Recommended improvements prioritized by severity
3. Architecture document to understand system design

## 📄 License

Not specified in repository.

## 🔗 Related

- [Songkick Website](https://www.songkick.com/)
- [Songkick API Documentation](https://www.songkick.com/developer)

---

**Analysis Date**: December 2025  
**Analysis Version**: 1.0  
**Repository Health**: 6.5/10 - Functional but needs hardening
