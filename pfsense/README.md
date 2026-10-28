# Listes pfSense

Listes de sites à bloquer, consommées par pfBlockerNG (feeds DNSBL) via leur URL « raw » :

    https://raw.githubusercontent.com/iopsthecloud/trano/main/pfsense/<fichier>.txt

Format : un domaine par ligne (`exemple.com`), commentaires en `#`.

## `doh-ipv4.txt` (généré, ne pas éditer)

Adresses IPv4 des résolveurs DoH publics, utilisées par l'alias pfSense `doh_servers`
(URL Table) pour rejeter le DoH sur le port 443. Générée chaque jour par la GitHub Action
`Liste DoH pfSense` (`scripts/build_doh_list.py`) depuis
[dibdot/DoH-IP-blocklists](https://github.com/dibdot/DoH-IP-blocklists), **moins les plages
Cloudflare** (adresses partagées avec des sites ordinaires) et les plages de
`doh-exclusions.txt`. Pour débloquer un site cassé : ajouter sa plage dans
`doh-exclusions.txt`.
