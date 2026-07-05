#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HACKWEB - Outil de modification de contenu web en temps réel
Développé par les Hacker Tchadien
"""

import sys
import re
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser

class HackWeb:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.modifications = []
        
    def fetch_url(self, url):
        """Récupère le contenu d'une URL"""
        try:
            # Création du contexte SSL pour éviter les erreurs de certificat
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
                return content
        except urllib.error.URLError as e:
            print(f"[ERREUR] Impossible de récupérer {url}: {e}")
            return None
        except Exception as e:
            print(f"[ERREUR] {e}")
            return None
    
    def add_modification(self, pattern, replacement):
        """Ajoute une règle de modification"""
        self.modifications.append((pattern, replacement))
        print(f"[+] Modification ajoutée: '{pattern}' -> '{replacement}'")
    
    def modify_content(self, content):
        """Applique toutes les modifications au contenu"""
        modified = content
        for pattern, replacement in self.modifications:
            modified = re.sub(pattern, replacement, modified, flags=re.IGNORECASE)
        return modified
    
    def inject_script(self, content, script_code):
        """Injecte un script dans le contenu HTML"""
        script_tag = f"<script>{script_code}</script>"
        # Injection avant la balise </body> ou </head>
        if '</body>' in content:
            content = content.replace('</body>', f"{script_tag}\n</body>")
        elif '</head>' in content:
            content = content.replace('</head>', f"{script_tag}\n</head>")
        else:
            content = script_tag + "\n" + content
        return content
    
    def modify_links(self, content, base_url):
        """Modifie les liens relatifs en liens absolus"""
        def replace_link(match):
            href = match.group(1)
            if href.startswith(('http://', 'https://', '#', 'mailto:', 'javascript:')):
                return match.group(0)
            absolute_url = urljoin(base_url, href)
            return f'href="{absolute_url}"'
        
        content = re.sub(r'href="([^"]*)"', replace_link, content)
        return content
    
    def save_content(self, content, filename="modified_page.html"):
        """Sauvegarde le contenu modifié"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[+] Contenu sauvegardé dans: {filename}")
            return True
        except Exception as e:
            print(f"[ERREUR] Impossible de sauvegarder: {e}")
            return False
    
    def display_info(self):
        """Affiche les informations du script"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    HACKWEB v1.0                              ║
║         Développé par les Hacker Tchadien                    ║
║                                                              ║
║  Outil de modification de contenu web en temps réel          ║
╚══════════════════════════════════════════════════════════════╝
        """)

def main():
    hackweb = HackWeb()
    hackweb.display_info()
    
    if len(sys.argv) < 2:
        print("Usage: python HACKWEB.py <URL> [options]")
        print("\nOptions:")
        print("  -o <fichier>    Sauvegarder dans un fichier spécifique")
        print("  -r <regex> <remplacement>  Remplacer un pattern par un autre")
        print("\nExemples:")
        print("  python HACKWEB.py https://example.com")
        print("  python HACKWEB.py https://example.com -o ma_page.html")
        print("  python HACKWEB.py https://example.com -r 'Example' 'HACKED'")
        return
    
    url = sys.argv[1]
    output_file = "modified_page.html"
    
    # Traitement des arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '-o' and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '-r' and i + 2 < len(sys.argv):
            hackweb.add_modification(sys.argv[i + 1], sys.argv[i + 2])
            i += 3
        else:
            i += 1
    
    print(f"[*] Récupération de: {url}")
    content = hackweb.fetch_url(url)
    
    if content:
        print(f"[+] Contenu récupéré: {len(content)} caractères")
        
        # Modification des liens relatifs
        content = hackweb.modify_links(content, url)
        
        # Application des modifications personnalisées
        if hackweb.modifications:
            print("[*] Application des modifications...")
            content = hackweb.modify_content(content)
        
        # Sauvegarde
        hackweb.save_content(content, output_file)
        
        print("\n[+] Opération terminée avec succès!")
        print(f"[*] Fichier sauvegardé: {output_file}")
    else:
        print("[-] Échec de la récupération du contenu")

if __name__ == "__main__":
    main()
