# HACKWEB

**Développé par les Hacker Tchadien**

HACKWEB est un script Python puissant qui permet de récupérer le code source d'une page web via son URL et de modifier ce code en temps réel. Il offre une interface interactive en ligne de commande pour appliquer différentes transformations sur le HTML, le CSS et le JavaScript.

## Fonctionnalités

- **Récupération de code source** : Télécharge le code HTML complet d'une page web depuis son URL
- **Modification de texte** : Remplace n'importe quel texte dans le code source par un autre
- **Modification de balises** : Change les noms des balises HTML (ex: `<div>` → `<section>`)
- **Modification d'attributs** : Modifie les attributs des balises HTML (ex: `class="old"` → `class="new"`)
- **Sauvegarde** : Enregistre le code modifié dans un fichier local

## Prérequis

- Python 3.7 ou supérieur
- Bibliothèques Python : `requests`, `beautifulsoup4`

## Installation

1. Clonez ou téléchargez ce repository
2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

Lancez le script depuis votre terminal :

```bash
python HACKWEB.py
```

Suivez ensuite les instructions à l'écran :
1. Entrez l'URL du site web à modifier
2. Choisissez le type de modification (texte, balise ou attribut)
3. Entrez l'ancienne valeur et la nouvelle valeur
4. Le code modifié sera affiché et sauvegardé dans un fichier

## Exemple

```
========================================
     HACKWEB - Développé par les Hacker Tchadien
========================================

Entrez l'URL du site web à modifier : https://example.com

Options de modification :
1. Modifier du texte
2. Modifier une balise HTML
3. Modifier un attribut HTML

Choisissez une option (1-3) : 1
Entrez le texte à remplacer : Example Domain
Entrez le nouveau texte : HACKED by Hacker Tchadien

Code source modifié :
[...]

Code source modifié sauvegardé dans : modified_page.html
```

## Avertissement

**Ce script est fourni à des fins éducatives et de test uniquement.**

L'utilisation de ce script sur des sites web sans autorisation explicite est illégale et peut entraîner des poursuites judiciaires. Les auteurs ne sont pas responsables de toute utilisation abusive de cet outil. Utilisez-le uniquement sur des sites dont vous êtes propriétaire ou pour lesquels vous avez obtenu une autorisation écrite.

## Développeurs

- **Hacker Tchadien** - Concepteur et développeur principal

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
