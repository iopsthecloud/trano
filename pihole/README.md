# Listes Pi-hole

Listes custom consommées par les Pi-hole (dont celui de Home Assistant), abonnés via leur URL « raw » :

    https://raw.githubusercontent.com/iopsthecloud/trano/main/pihole/<fichier>.txt

Format : un domaine par ligne (`exemple.com`, correspondance exacte) ou ABP (`||exemple.com^`, domaine + sous-domaines), commentaires en `#`. Les regex ne sont pas acceptées dans une liste abonnée : elles se gèrent dans la denylist locale de Pi-hole.
