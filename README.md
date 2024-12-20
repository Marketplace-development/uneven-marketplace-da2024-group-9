# Kotrepair
### Beschrijving
Dit project betreft een eindwerk voor het vak programmeren te UGent. De inhoud van het project bestaat uit een full-stack flask applicatie, waarbij de database gehost wordt via Supabase, de backend bestaat uit het Flask framework & de frontend bestaat uit templates.

---

### Setup
#### .env file
Een .env file is een bestand waarin omgevingsvariabelen zitten. Deze file bevat meestal vrij gevoelige data die je niet zomaar in je code wilt zetten, of op Github wilt delen. 

Via de ingebouwde Python package **os** kan je via de key van de omgevingsvariabele de waardes ophalen uit die file (eigenlijk leest die os package die hele file in en slaat hij achterliggend een dictionary op met alle key-values). 

De noodzakelijke omgevingsvariabelen die je lokaal moet instellen opdat de applicatie correct zou runnen zijn:
- FLASK_SECRET_KEY
    - Dit is een random string dat Flask verwacht om je applicatie 'uniek' te maken. Dit mag in principe alles zijn, verzin iets leuks of genereer een uuid online
- SUPABASE_URL
    - Dit is de connection URL die je via Supabase kan vinden. Let op: Standaard biedt Supabase geen IPV4 connecties aan voor directe verbindingen (Direct Connection). Om toch via IPV4 te verbinden met Supabase gebruik je best de Session Pooler string. 
    - **Hoe vind ik deze Supabase connection string?**
        1. Log in op Supabase
        2. In het navigatiemenu links klik je op 'Project Settings'
        3. Bovenaan je scherm zie je normaal een knop 'Connect' met een stekker icoontje naast, klik hierop
        4. Onder de tab **Connection String** zorg je dat je als type 'URI' geselecteerd hebt en kopieer dan je **Session Pooler** string. Je zult in deze string wel nog [YOUR-PASSWORD] moeten vervangen door je database wachtwoord
        5. Weet je je database wachtwoord niet meer? Niet getreurd. Via **Project Settings > Database > Database Password** kan je deze weer resetten.
    - Vb: postgresql://postgres.xxx:[PASSWORD]@aws-0-eu-west-3.pooler.supabase.com:5432/postgres


</br>

#### Virtual environment (venv)
Om het project op te zetten, zullen we gebruik maken van virtual environments (ook wel venv genoemd). Virtual environments zijn ideaal voor (groeps-)projecten zoals deze, waar er meerdere mensen aan werken. 

Via virtual environments zijn we zeker dat elke gebruiker/developer/... dezelfde python omgeving benuttigd met dezelfde packages, op dezelfde versies. (Alternatieve manieren om venvs op te zetten zijn Anaconda/Poetry/...)

1. Zorg ervoor dat je Python 3.10 of hoger geïnstalleerd hebt.
2. Maak een virtuele omgeving aan:
    - python3 -m venv venv **OF** python -m venv venv
    - *Dit zal een venv folder creëren in het project, via de .gitignore file zal deze genegeerd worden bij het pushen naar Github*
3. 🟢Activeer de virtuele omgeving:
    - Linux/Mac: `source venv/bin/activate`
    - Windows: `venv\Scripts\activate`
4. ⬇️Installeer de vereisten, in deze requirements.txt file staan alle benodigde packages en hun versies:
    - pip install -r requirements.txt
5. 🔴 Wil je uit de virtuele omgeving gaan? Deactiveer de virtuele omgeving na gebruik met `deactivate`. 

</br>

Figma:![image](https://github.com/user-attachments/assets/2f7c5516-4300-4a2a-8a97-510fefdad016)

