from checker import (
    SITES,
    build_url,
    check_headers,
    check_site,
    is_https,
    retry_check,
    scan_sites,
    show_response,
)


def main():
    # Partea 1 - construire URL si verificare HTTPS
    print("Partea 1")
    host = SITES[0].replace("https://", "")
    print(build_url(host, "pagina"))
    print(build_url(host, "/pagina"))
    print(is_https(SITES[0]))
    print(is_https("http://example.com"))

    # Partea 2 - cerere HTTP simpla
    print("\nPartea 2")
    show_response(SITES[0])
    show_response(SITES[6])
    show_response(SITES[9])

    # Partea 3 - date despre un site
    print("\nPartea 3")
    print(check_site(SITES[0]))
    print(check_site(SITES[6]))
    print(check_site(SITES[9]))

    # Partea 4 - scanare site-uri
    print("\nPartea 4")
    scan_sites()

    # Partea 5 - anteturi de securitate
    print("\nPartea 5")
    print(check_headers(SITES[10]))
    print(check_headers(SITES[11]))
    print(check_headers(SITES[9]))

    # Partea 6 - retry check
    print("\nPartea 6")
    print(retry_check(SITES[6]))
    print(retry_check(SITES[7], attempts=2))
    print(retry_check(SITES[9]))


if __name__ == "__main__":
    main()
