import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    host = host.strip()
    path = path.strip()
    if not path:
        return "https://" + host.rstrip("/") + "/"
    return "https://" + host.rstrip("/") + "/" + path.lstrip("/")


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.lower().startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=5)
        print("Cod HTTP:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type", "unknown"))
    except requests.RequestException as error:
        print("Eroare la cerere:", type(error).__name__)


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "unknown"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }
    except requests.RequestException as error:
        return {"status": None, "error": type(error).__name__}


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []
    successful = []
    failed = 0

    for url in SITES:
        result = check_site(url)
        item = {"url": url}
        item.update(result)
        results.append(item)

        if result.get("status") == 200:
            successful.append(item)
        else:
            failed += 1

    successful.sort(key=lambda x: x["length"], reverse=True)

    print("Site-uri cu status 200:")
    for site in successful:
        print(f"{site['url']} - {site['length']} octeti")

    print("Site-uri reusite:", len(successful))
    print("Site-uri esuate:", failed)
    return results


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response = requests.get(url, timeout=5)
        headers = {name.lower() for name in response.headers}

        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header.lower() in headers:
                present.append(header)
            else:
                missing.append(header)

        score = int((len(present) / len(SECURITY_HEADERS)) * 100) if SECURITY_HEADERS else 0
        return {"present": present, "missing": missing, "score": score}
    except requests.RequestException as error:
        return {"status": None, "error": type(error).__name__}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    last_status = None
    last_error = None
    total = 0

    for _ in range(attempts):
        total += 1
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            if last_status < 500:
                return {"status": last_status, "attempts": total}
        except requests.RequestException as error:
            last_error = type(error).__name__

    result = {"status": last_status, "attempts": total}
    if last_error is not None:
        result["error"] = last_error
    return result
