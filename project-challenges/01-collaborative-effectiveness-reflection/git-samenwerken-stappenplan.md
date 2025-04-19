# GitHub Samenwerken via Pull Requests

> Laatst bijgewerkt: 2025-04-17

## 🧩 Overzicht
Werk samen aan een project door via pull requests code van elkaar te reviewen en samen te voegen.

---

## 🔧 Stap 1: Repository aanmaken (door eigenaar)

1. Maak een nieuwe **private** repository op GitHub.
2. Voeg een README toe (optioneel).
3. Voeg je partner toe via **Settings → Collaborators → Add people**.
4. De partner accepteert de uitnodiging.

---

## 💻 Stap 2: Repository klonen (door partner)

```bash
git clone https://github.com/jouwgebruikersnaam/reponaam.git
cd reponaam
```

> Vervang de link met de juiste URL van de repo.

---

## 🌿 Stap 3: Nieuwe branch maken (voor wijzigingen)

```bash
git checkout -b feature-naam
```

Bijvoorbeeld:

```bash
git checkout -b knop-verbetering
```

---

## ✍️ Stap 4: Wijzigingen doen, committen en pushen

Na het aanpassen van de code:

```bash
git add .
git commit -m "Verbeterde de logica van de knop"
git push origin knop-verbetering
```

---

## 🔄 Stap 5: Pull Request aanmaken

1. Ga naar de GitHub-pagina van de repo.
2. Klik op **"Compare & pull request"**.
3. Beschrijf wat je hebt gedaan.
4. Klik op **"Create pull request"**.

---

## ✅ Stap 6: Review en merge

Door de eigenaar van de repo:

1. Bekijk de pull request.
2. Geef opmerkingen of keur goed.
3. Klik op **"Merge pull request"** → **"Confirm merge"**.
4. Verwijder eventueel de branch.

---

## 🔄 Stap 7: Repository up-to-date houden

Iedereen doet voor nieuwe aanpassingen:

```bash
git pull origin main
```

---
