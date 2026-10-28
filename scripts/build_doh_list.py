#!/usr/bin/env python3
"""Construit pfsense/doh-ipv4.txt : résolveurs DoH publics moins les plages CDN partagées.

Source : dibdot/DoH-IP-blocklists (doh-ipv4.txt). On retire toute adresse incluse dans les
plages IPv4 publiées par Cloudflare (https://www.cloudflare.com/ips-v4) et dans
pfsense/doh-exclusions.txt : ces adresses servent aussi des sites ordinaires, les bloquer
sur le port 443 casserait la navigation.
"""
import ipaddress
import sys
import urllib.request
from pathlib import Path

DOH_URL = "https://raw.githubusercontent.com/dibdot/DoH-IP-blocklists/master/doh-ipv4.txt"
CLOUDFLARE_URL = "https://www.cloudflare.com/ips-v4"
ROOT = Path(__file__).resolve().parent.parent
EXCLUSIONS = ROOT / "pfsense" / "doh-exclusions.txt"
OUTPUT = ROOT / "pfsense" / "doh-ipv4.txt"


def fetch(url):
    # Cloudflare refuse l'agent HTTP par défaut de urllib (403).
    req = urllib.request.Request(url, headers={"User-Agent": "gh-trano-doh-list/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode()


def networks(text):
    """Extrait les réseaux IPv4 d'un texte, en ignorant commentaires et lignes vides."""
    nets = []
    for line in text.splitlines():
        token = line.split("#", 1)[0].strip()
        if token:
            nets.append(ipaddress.ip_network(token, strict=False))
    return nets


def main():
    doh = networks(fetch(DOH_URL))
    excluded = networks(fetch(CLOUDFLARE_URL))
    if EXCLUSIONS.exists():
        excluded += networks(EXCLUSIONS.read_text())
    if len(doh) < 500 or not excluded:
        sys.exit(f"source suspecte : {len(doh)} entrées DoH, {len(excluded)} exclusions")

    kept = sorted(
        {n for n in doh if not any(n.subnet_of(e) for e in excluded)},
        key=lambda n: (int(n.network_address), n.prefixlen),
    )
    body = "\n".join(str(n.network_address) if n.prefixlen == 32 else str(n) for n in kept)
    OUTPUT.write_text(
        "# Résolveurs DoH publics (IPv4) à bloquer sur 443, plages CDN partagées retirées.\n"
        f"# Généré par scripts/build_doh_list.py depuis {DOH_URL}\n"
        f"# {len(kept)} entrées conservées, {len(doh) - len(kept)} retirées.\n"
        f"{body}\n"
    )
    print(f"{len(kept)} entrées conservées, {len(doh) - len(kept)} retirées")


if __name__ == "__main__":
    main()
