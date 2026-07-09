#!/usr/bin/env python3

import sys
import socket
from urllib.parse import urlparse


def clean_hostname(url):
    """Extract hostname from a URL or plain domain."""
    if "://" not in url:
        url = "http://" + url

    parsed = urlparse(url)
    hostname = parsed.hostname

    if not hostname:
        raise ValueError("Invalid website address")

    return hostname


def lookup_dns(hostname):
    """Return all IPv4 and IPv6 addresses for a hostname."""
    results = set()

    try:
        records = socket.getaddrinfo(
            hostname,
            None,
            socket.AF_UNSPEC,
            socket.SOCK_STREAM
        )

        for record in records:
            ip = record[4][0]
            results.add(ip)

    except socket.gaierror as e:
        raise RuntimeError(f"DNS lookup failed: {e}")

    return sorted(results)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <website>")
        print(f"Example: {sys.argv[0]} example.com")
        sys.exit(1)

    try:
        hostname = clean_hostname(sys.argv[1])

        print(f"\nDNS lookup for: {hostname}")
        print("-" * 40)

        ips = lookup_dns(hostname)

        if not ips:
            print("No IP addresses found.")
            sys.exit(1)

        for i, ip in enumerate(ips, start=1):
            print(f"{i}. {ip}")

        print("-" * 40)
        print(f"Total addresses found: {len(ips)}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()