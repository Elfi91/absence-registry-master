# 🎓 School Registry API – Gestione Presenze

Questo progetto è una REST API sviluppata in **Django** per la gestione automatizzata delle presenze e delle assenze dei partecipanti al corso. Il sistema permette di monitorare l'andamento del corso, distinguendo tra amministratori e partecipanti, e calcolando automaticamente le statistiche di presenza.

## 👥 Il Team
* **Chiara**: Security, Ruoli Utente e Permessi (Branch: `feature/auth-permissions`).
* **Elisabetta**: Business Logic, Calcolo Percentuali e Statistiche (Branch: `feature/presence-stats`).
* **Paola**: Gestione Profili e Integrazione Admin (Branch: `feature/profile-management`).

## ✨ Funzionalità Principali

* **Autenticazione JWT**: Registrazione e login sicuri tramite JSON Web Tokens.
* **Dashboard Partecipante**: Ogni studente può visualizzare esclusivamente le proprie assenze e la propria percentuale di presenza.
* **Area Admin**: Gli amministratori hanno il controllo completo per aggiungere, modificare o eliminare record di qualsiasi partecipante.
* **Calcolo Dinamico**: La percentuale di presenza viene calcolata in tempo reale basandosi solo sulle giornate di corso già trascorse, escludendo automaticamente le date future.

## 🛠️ Tecnologie Utilizzate
* **Python**: Linguaggio di programmazione core.
* **Django & Django REST Framework**: Framework per lo sviluppo del backend e delle API.
* **SimpleJWT**: Gestione dei token di autenticazione.
* **SQLite**: Database utilizzato per lo sviluppo locale.

## 🚀 Installazione e Setup

1.  **Clona il repository:**
    ```bash
    git clone <repository_url>
    cd registro_assenze
    ```

2.  **Crea e attiva un ambiente virtuale:**
    * **macOS/Linux:**
        ```bash
        python -m venv .venv
        source .venv/bin/activate
        ```
    * **Windows:**
        ```bash
        python -m venv .venv
        .\.venv\Scripts\activate
        ```

3.  **Installa le dipendenze:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Esegui le migrazioni del database:**
    ```bash
    python manage.py migrate
    ```

5.  **Avvia il server di sviluppo:**
    ```bash
    python manage.py runserver
    ```
    L'API sarà disponibile all'indirizzo `http://127.0.0.1:8000/`.

## 📡 Endpoint API Principali

| Metodo | Endpoint | Descrizione | Accesso |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/login/` | Login e ricezione token JWT | Pubblico |
| `GET` | `/api/students/` | Lista studenti e % presenza | Admin/User |
| `POST` | `/api/absences/` | Crea un record di assenza | Solo Admin |
| `GET` | `/api/absences/<id>/` | Dettaglio specifica assenza | Admin/Owner |
| `PATCH` | `/api/students/me/` | Aggiornamento profilo personale | Partecipante |

---
*Progetto realizzato come esercitazione per il corso di AWS Re/Start 2025/26.*