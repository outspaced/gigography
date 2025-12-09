# Gigography Scraper Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Gigography Scraper                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
        ▼                                       ▼
┌──────────────────┐                 ┌──────────────────┐
│  songkick.py     │                 │  songkick.sh     │
│  (Web Scraper)   │                 │  (API Client)    │
└──────────────────┘                 └──────────────────┘
        │                                       │
        │                                       │
        ▼                                       ▼
┌──────────────────┐                 ┌──────────────────┐
│   Songkick       │                 │   Songkick API   │
│   Web Pages      │                 │   (XML/JSON)     │
└──────────────────┘                 └──────────────────┘
        │                                       │
        │                                       │
        ▼                                       ▼
┌──────────────────┐                 ┌──────────────────┐
│   CSV Output     │                 │   XML Files      │
│   gigography.csv │                 │   0.xml-12.xml   │
└──────────────────┘                 └──────────────────┘
```

## Python Script Flow (songkick.py)

```
START
  │
  ├─► Initialize variables
  │   • gigs = []
  │   • current_page = 1
  │   • unique_gig_keys = set()
  │
  ├─► Enter pagination loop
  │   │
  │   ├─► Build URL with page number
  │   │
  │   ├─► Make HTTP GET request
  │   │   └─► Include User-Agent header
  │   │
  │   ├─► Parse HTML with BeautifulSoup
  │   │
  │   ├─► Find JSON-LD scripts
  │   │   │
  │   │   └─► For each script:
  │   │       ├─► Parse JSON data
  │   │       └─► Filter MusicEvent types
  │   │
  │   ├─► Extract event details
  │   │   ├─► Date (startDate)
  │   │   ├─► Event Name (name)
  │   │   ├─► Venue (location.name)
  │   │   └─► Location (addressLocality, addressCountry)
  │   │
  │   ├─► Check for duplicates
  │   │   └─► Using key: "date|event_name|venue"
  │   │
  │   ├─► Add to gigs list if unique
  │   │
  │   ├─► If no new gigs found → BREAK
  │   │
  │   ├─► Increment page counter
  │   │
  │   └─► Sleep 1.5 seconds (rate limiting)
  │
  ├─► Write results to CSV
  │   ├─► Open file with UTF-8 encoding
  │   ├─► Write header row
  │   └─► Write data rows
  │
END
```

## Data Structure

### Input: JSON-LD Structure
```json
{
  "@type": "MusicEvent",
  "name": "Artist Name @ Venue Name",
  "startDate": "2025-11-26T19:30:00",
  "location": {
    "name": "Barbican Centre",
    "address": {
      "addressLocality": "London",
      "addressCountry": "UK"
    }
  }
}
```

### Output: CSV Structure
```csv
Date,Event Name,Venue,Location
2025-11-26,Artist @ Venue,Venue Name,"London, UK"
```

## Component Details

### 1. HTTP Request Handler
- **Library**: `requests`
- **Features**: 
  - Custom User-Agent
  - Error handling for HTTP errors
  - Connection error handling
- **Missing**: Timeout, retry logic

### 2. HTML Parser
- **Library**: `BeautifulSoup4`
- **Target**: JSON-LD structured data
- **Advantages**: 
  - Reliable (structured data)
  - No brittle CSS selectors
- **Limitations**: Depends on Songkick using JSON-LD

### 3. Data Processor
- **Duplicate Detection**: Set-based O(1) lookup
- **Key Format**: `"{date}|{event_name}|{venue}"`
- **Transformation**: JSON → Dictionary → CSV row

### 4. File Writer
- **Format**: CSV with UTF-8 encoding
- **Fields**: Date, Event Name, Venue, Location
- **Safety**: Context manager (with statement)

## Bash Script Flow (songkick.sh)

```
START
  │
  ├─► Loop: i from 0 to 10
  │   │
  │   └─► For each iteration:
  │       ├─► Build API URL
  │       │   • Base: api.songkick.com
  │       │   • User: outspaced
  │       │   • Page: $i
  │       │   • API Key: $SONGKICK_API_KEY
  │       │
  │       ├─► Execute curl
  │       │   • Method: GET
  │       │   • Data: page & apikey params
  │       │
  │       └─► Save output to {i}.xml
  │
END
```

## Error Handling

### Python Script

```
Try/Catch Blocks:
├─► JSON parsing errors → continue (silent)
├─► Event parsing errors → log & continue
├─► HTTP errors → print message & break
├─► Request exceptions → print message & break
└─► CSV write errors → print message
```

### Bash Script

```
Error Handling: NONE
├─► curl failures → ignored
├─► missing API key → empty parameter
├─► network issues → ignored
└─► file write errors → ignored
```

## Dependencies Graph

```
songkick.py
    ├── requests
    ├── beautifulsoup4
    └── Standard Library
        ├── csv
        ├── time
        ├── json
        └── typing

songkick.sh
    └── System Tools
        ├── curl
        ├── bash
        └── seq
```

## Rate Limiting Strategy

### Python Script
- **Delay**: 1.5 seconds between requests
- **Method**: `time.sleep(1.5)`
- **Reason**: Prevent server overload, avoid IP blocking

### Bash Script
- **Delay**: None
- **Risk**: Could trigger rate limiting or IP blocking

## Pagination Strategy

### Python Script
- **Method**: Automatic detection
- **Stop Condition**: No new unique gigs found
- **Advantage**: Adapts to any number of pages

### Bash Script
- **Method**: Fixed range (0-10)
- **Stop Condition**: After page 10
- **Limitation**: May fetch too few or too many pages

## Output Files

```
Repository Root
├── songkick.py              # Python scraper
├── songkick.sh              # Bash API client
├── songkick_gigography.csv  # Python output (CSV)
├── 0.xml - 12.xml          # Bash output (XML files)
├── 0.html - 12.html        # Cached HTML pages (optional)
└── *.json                   # Intermediate data (optional)
```

## Security Considerations

### Threat Model

```
Threats:
├── Path Traversal
│   └── Impact: Malicious filename could write to sensitive locations
│
├── API Key Exposure (bash)
│   ├── Process list visibility
│   ├── Shell history logging
│   └── Server access logs
│
├── Network Interception
│   └── Impact: Low (read-only scraping of public data)
│
└── Resource Exhaustion
    └── Impact: Infinite loop without page limit
```

## Performance Characteristics

```
Metrics (Python Script):
├── Requests/second: ~0.67 max (1.5s delay between requests)
├── Memory usage: O(n) where n = number of gigs
├── Network bandwidth: ~280KB per page (HTML)
└── Disk I/O: Single write at completion

Metrics (Bash Script):
├── Requests/second: ~10+ (no delay)
├── Memory usage: O(1) (streaming to files)
├── Network bandwidth: Varies (XML response size)
└── Disk I/O: One write per page
```

## Future Improvements

### Architecture Enhancements

1. **Configuration Management**
   ```
   config.yaml
   ├── api_key
   ├── user_id
   ├── rate_limit
   └── output_format
   ```

2. **Modular Design**
   ```
   src/
   ├── scraper.py      # Core scraping logic
   ├── parser.py       # HTML/JSON parsing
   ├── exporter.py     # CSV/JSON export
   └── config.py       # Configuration handling
   ```

3. **Database Storage**
   ```
   SQLite DB
   ├── gigs table
   ├── venues table
   └── artists table
   ```

4. **API Client**
   ```
   REST API wrapper
   ├── Authentication
   ├── Rate limiting
   ├── Error handling
   └── Response parsing
   ```

## Conclusion

The architecture is straightforward and functional for a scraping utility:
- **Strengths**: Simple, maintainable, works well for the use case
- **Weaknesses**: Lacks modularity, error recovery, and advanced features
- **Recommendation**: Good for personal use, needs hardening for production

For more details, see the individual analysis documents.
