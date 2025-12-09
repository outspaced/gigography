# Shell Script Analysis: songkick.sh

## Overview

**File**: `songkick.sh`
**Purpose**: Download gigography data from Songkick API using curl
**Language**: Bash

## Code Content

```bash
#!/bin/bash
for i in `seq 0 10`;
do
	curl -G -d "page=$i&apikey=$SONGKICK_API_KEY" https://api.songkick.com/api/3.0/users/outspaced/gigography.xml > $i.xml
done
```

## Issues and Recommendations

### 🔴 Critical Issues

#### 1. **Unquoted Variables**
- **Location**: Lines 2 and 4 (loop variable and output redirection)
- **Issue**: `$i` and `$SONGKICK_API_KEY` are not quoted in the curl command
- **Risk**: Will break if values contain spaces or special characters
- **Fix**: Use `"$i"` and properly quote variable expansions in the curl command

#### 2. **No Error Checking**
- **Issue**: Script doesn't check if curl commands succeed
- **Impact**: Failed downloads go unnoticed
- **Recommendation**: Add `set -e` at the start or check `$?` after curl

#### 3. **Command Substitution with Backticks**
- **Location**: Loop initialization (`` `seq 0 10` ``)
- **Issue**: Old-style command substitution using backticks (deprecated style)
- **Recommendation**: Use modern syntax: `$(seq 0 10)`

#### 4. **Missing API Key Validation**
- **Issue**: No check if `$SONGKICK_API_KEY` is set
- **Impact**: Makes API calls with empty key, wasting time
- **Recommendation**: Add validation at start of script

#### 5. **Hardcoded Username**
- **Issue**: User `outspaced` is hardcoded in API URL
- **Impact**: Not reusable for other users
- **Recommendation**: Accept username as parameter or environment variable

### 🟡 Medium Priority Issues

#### 6. **No Output Directory Control**
- **Issue**: Files written to current directory
- **Impact**: Could clutter working directory
- **Recommendation**: Allow output directory specification

#### 7. **Overwriting Files Without Warning**
- **Issue**: `> $i.xml` will overwrite existing files
- **Impact**: Data loss if run multiple times
- **Recommendation**: Add warning or timestamp to filenames

#### 8. **No Progress Indication**
- **Issue**: Silent execution, no feedback
- **Impact**: User doesn't know if script is working
- **Recommendation**: Add echo statements or use curl's progress bar

#### 9. **Hard-Coded Page Range**
- **Issue**: Always downloads pages 0-10
- **Impact**: Inflexible, may fetch too many or too few pages
- **Recommendation**: Accept range as parameters

### 🟢 Low Priority Issues

#### 10. **No Shebang Options**
- **Recommendation**: Consider adding `#!/bin/bash -e` for fail-fast behavior

#### 11. **No Usage Documentation**
- **Issue**: No comments explaining what script does
- **Recommendation**: Add header comments with usage instructions

#### 12. **Inconsistent Indentation**
- **Issue**: Mix of tabs (appears as tabs)
- **Recommendation**: Use consistent spaces (2 or 4)

## Security Concerns

### 🔒 Security Issues

#### 1. **API Key in URL (HIGH RISK)**
- **Issue**: API key passed in URL parameters via `-d` flag
- **Risk**: 
  - Appears in shell history
  - May appear in server logs
  - Visible in process list (`ps aux`)
- **Severity**: HIGH
- **Note**: This may be unavoidable if the Songkick API requires the key as a query parameter. Check API documentation for alternative authentication methods.
- **Mitigation**: At minimum, document this security consideration

#### 2. **No HTTPS Verification**
- **Issue**: curl doesn't explicitly verify SSL certificates
- **Risk**: Man-in-the-middle attacks possible
- **Recommendation**: Add `--cacert` or ensure curl's default cert bundle is used

#### 3. **Environment Variable Exposure**
- **Issue**: `$SONGKICK_API_KEY` could be exposed through environment
- **Recommendation**: Document secure handling, consider reading from secure file

## Improved Version

Here's a suggested improved version:

```bash
#!/bin/bash -e

# Download gigography data from Songkick API
# Usage: ./songkick.sh [username] [start_page] [end_page] [output_dir]

set -euo pipefail

# Configuration
USERNAME="${1:-outspaced}"
START_PAGE="${2:-0}"
END_PAGE="${3:-10}"
OUTPUT_DIR="${4:-.}"

# Validate API key
if [[ -z "${SONGKICK_API_KEY:-}" ]]; then
    echo "Error: SONGKICK_API_KEY environment variable not set" >&2
    echo "Usage: export SONGKICK_API_KEY='your_key_here'" >&2
    exit 1
fi

# Create output directory if needed
mkdir -p "$OUTPUT_DIR"

echo "Downloading gigography for user: $USERNAME"
echo "Pages: $START_PAGE to $END_PAGE"
echo "Output directory: $OUTPUT_DIR"

# Download pages
for i in $(seq "$START_PAGE" "$END_PAGE"); do
    output_file="$OUTPUT_DIR/$i.xml"
    echo "Downloading page $i..."
    
    if curl -f -s -G \
        -d "page=$i" \
        -d "apikey=$SONGKICK_API_KEY" \
        "https://api.songkick.com/api/3.0/users/$USERNAME/gigography.xml" \
        > "$output_file"; then
        echo "✓ Page $i downloaded successfully"
    else
        echo "✗ Failed to download page $i" >&2
        exit 1
    fi
    
    # Rate limiting
    sleep 0.5
done

echo "Download complete! Files saved to: $OUTPUT_DIR"
```

## Comparison: Original vs Improved

| Aspect | Original | Improved |
|--------|----------|----------|
| Error handling | None | Exit on error, check curl status |
| Flexibility | Hardcoded values | Command-line parameters |
| Security | API key in URL | Still in URL (API limitation) |
| User feedback | Silent | Progress messages |
| Validation | None | API key check, directory creation |
| Quotes | Missing | Properly quoted |
| Command substitution | Backticks | Modern `$()` syntax |

## Conclusion

The original `songkick.sh` script is functional but has several issues:

- **Security**: API key exposure in URL and process list
- **Reliability**: No error checking or validation
- **Usability**: Hardcoded values, no feedback
- **Maintainability**: Old syntax, no documentation

**Severity**: The security issue with API key exposure is the most concerning. While this may be unavoidable with Songkick's API design, the script should at least document this risk.

**Recommendation**: Update to the improved version or migrate to using the Python script (`songkick.py`) which has better structure and error handling.

**Overall Assessment: Needs Improvement** ⭐⭐☆☆☆ (2/5)
