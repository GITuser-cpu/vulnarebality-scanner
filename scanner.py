import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Common payloads for SQL Injection and XSS testing
SQLI_PAYLOADS = ["'", "\"", "' OR '1'='1", "\" OR \"1\"=\"1", "';--", "\";--"]
XSS_PAYLOADS = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>", "<svg/onload=alert('XSS')>"]

def get_url_with_payload(url, param, payload):
    """
    Return a new URL with the given payload injected into the specified parameter.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if param in query_params:
        query_params[param] = [payload]
    else:
        query_params[param] = [payload]
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))
    return new_url

def test_sqli(url):
    """
    Test the URL for SQL Injection vulnerabilities by injecting payloads into parameters.
    """
    print("[*] Testing for SQL Injection vulnerabilities...")
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    vulnerable_params = []

    if not query_params:
        print("[-] No query parameters found to test for SQL Injection.")
        return vulnerable_params

    for param in query_params:
        for payload in SQLI_PAYLOADS:
            test_url = get_url_with_payload(url, param, payload)
            try:
                response = requests.get(test_url, timeout=10)
                if is_sqli_vulnerable(response.text):
                    print(f"[!] Possible SQL Injection vulnerability detected in parameter: {param} with payload: {payload}")
                    vulnerable_params.append(param)
                    break
            except requests.RequestException as e:
                print(f"[-] Request error for {test_url}: {e}")
    if not vulnerable_params:
        print("[+] No SQL Injection vulnerabilities detected.")
    return vulnerable_params

def is_sqli_vulnerable(response_text):
    """
    Basic heuristic to detect SQL errors in response text.
    """
    errors = [
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
        "sql syntax error",
        "mysql_fetch_array()",
        "syntax error",
        "mysql_num_rows()",
        "pg_query()",
        "unterminated string constant",
    ]
    response_lower = response_text.lower()
    for error in errors:
        if error in response_lower:
            return True
    return False

def test_xss(url):
    """
    Test the URL for XSS vulnerabilities by injecting payloads into parameters.
    """
    print("[*] Testing for Cross-Site Scripting (XSS) vulnerabilities...")
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    vulnerable_params = []

    if not query_params:
        print("[-] No query parameters found to test for XSS.")
        return vulnerable_params

    for param in query_params:
        for payload in XSS_PAYLOADS:
            test_url = get_url_with_payload(url, param, payload)
            try:
                response = requests.get(test_url, timeout=10)
                if is_xss_vulnerable(response.text, payload):
                    print(f"[!] Possible XSS vulnerability detected in parameter: {param} with payload: {payload}")
                    vulnerable_params.append(param)
                    break
            except requests.RequestException as e:
                print(f"[-] Request error for {test_url}: {e}")
    if not vulnerable_params:
        print("[+] No XSS vulnerabilities detected.")
    return vulnerable_params

def is_xss_vulnerable(response_text, payload):
    """
    Check if the payload is reflected in the response text.
    """
    return payload in response_text

def main():
    print("Web Application Vulnerability Scanner")
    target_url = input("Enter the target URL (with parameters): ").strip()
    if not target_url:
        print("[-] No URL provided. Exiting.")
        return

    print(f"Scanning {target_url} ...")
    sqli_vulns = test_sqli(target_url)
    xss_vulns = test_xss(target_url)

    print("\nScan Summary:")
    if sqli_vulns:
        print(f"SQL Injection vulnerable parameters: {', '.join(sqli_vulns)}")
    else:
        print("No SQL Injection vulnerabilities found.")

    if xss_vulns:
        print(f"XSS vulnerable parameters: {', '.join(xss_vulns)}")
    else:
        print("No XSS vulnerabilities found.")

if __name__ == "__main__":
    main()

def run_scan(url):
    """
    Run SQLi and XSS tests on the given URL and return a string summary of results.
    """
    sqli_vulns = test_sqli(url)
    xss_vulns = test_xss(url)

    result_lines = []
    if sqli_vulns:
        result_lines.append(f"SQL Injection vulnerable parameters: {', '.join(sqli_vulns)}")
    else:
        result_lines.append("No SQL Injection vulnerabilities found.")

    if xss_vulns:
        result_lines.append(f"XSS vulnerable parameters: {', '.join(xss_vulns)}")
    else:
        result_lines.append("No XSS vulnerabilities found.")

    return "\\n".join(result_lines)
