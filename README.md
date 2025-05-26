# Web Application Vulnerability Scanner

This is a simple Python-based web application vulnerability scanner that detects common vulnerabilities such as SQL Injection and Cross-Site Scripting (XSS).

## Features

- Tests URL parameters for SQL Injection vulnerabilities using common payloads.
- Tests URL parameters for XSS vulnerabilities by injecting script payloads.
- Uses `requests` for HTTP requests and `BeautifulSoup` for HTML parsing.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

Install the required Python packages using pip:

```
pip install -r requirements.txt
```

## Usage

Run the scanner script and provide the target URL with parameters when prompted:

```
python scanner.py
```

Example target URL:

```
http://example.com/page.php?id=1&name=test
```

The scanner will test each parameter for SQL Injection and XSS vulnerabilities and print the results.

## Disclaimer

This tool is for educational and authorized testing purposes only. Do not use it to scan websites without permission.
