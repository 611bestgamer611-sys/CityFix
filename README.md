# CityFix - Sistema di Segnalazioni Comunali

CityFix è una piattaforma completa per la gestione delle segnalazioni comunali, costruita con architettura a microservizi.

## 📋 Indice

- [Architettura](#architettura)
- [Tecnologie Utilizzate](#tecnologie-utilizzate)
- [Requisiti di Sistema](#requisiti-di-sistema)
- [Installazione](#installazione)
- [Configurazione](#configurazione)
- [Avvio del Progetto](#avvio-del-progetto)
- [Struttura del Progetto](#struttura-del-progetto)
- [Servizi](#servizi)
- [Schema Database](#schema-database)
- [API Documentation](#api-documentation)

## 🏗️ Architettura

Il progetto utilizza un'architettura a microservizi con i seguenti componenti:

```
┌─────────────┐
│  CityFixUI  │ (React + Vite)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Orchestrator│ (API Gateway - FastAPI)
└──────┬──────┘
       │
       ├──────► AuthService (porta 8001)
       ├──────► AdminService (porta 8002)
       ├──────► TicketService (porta 8003)
       ├──────► MediaService (porta 8004)
       ├──────► GeoService (porta 8005)
       └──────► NotificationService (porta 8006)
                    │
                    ▼
              ┌───────────┐
              │  MongoDB  │
              └───────────┘
```

## 🛠️ Tecnologie Utilizzate

### Frontend
- **React 18+** - Framework UI
- **Vite** - Build tool e dev server
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - Componenti UI
- **React Router v6** - Routing
- **Axios** - HTTP client
- **React-Leaflet** - Mappe interattive con OpenStreetMap

### Backend
- **FastAPI 0.100+** - Framework web async
- **Python 3.11** - Linguaggio di programmazione
- **Motor** - Driver async MongoDB
- **Pydantic v2** - Data validation
- **Python-jose** - JWT authentication
- **Passlib + bcrypt** - Password hashing
- **HTTPX** - HTTP client async

### Database
- **MongoDB 7.0** - Database NoSQL

### Infrastructure
- **Docker** - Containerizzazione
- **Docker Compose** - Orchestrazione container

## 📋 Requisiti di Sistema

- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- **Node.js** >= 20 (per sviluppo locale frontend)
- **Python** >= 3.11 (per sviluppo locale backend)
- **MongoDB Compass** (opzionale, per visualizzare il database)

## 🚀 Installazione

### 1. Clonare il Repository

```bash
git clone <repository-url>
cd cityfix
```

### 2. Configurare le Variabili d'Ambiente

Copiare i file `.env.example` in `.env` per ogni servizio:

```bash
# Frontend
cp src/CityFixUI/.env.example src/CityFixUI/.env

# Backend Services
cp src/Orchestrator/.env.example src/Orchestrator/.env
cp src/AuthService/.env.example src/AuthService/.env
cp src/AdminService/.env.example src/AdminService/.env
cp src/TicketService/.env.example src/TicketService/.env
cp src/MediaService/.env.example src/MediaService/.env
cp src/GeoService/.env.example src/GeoService/.env
cp src/NotificationService/.env.example src/NotificationService/.env
```

### 3. Modificare le Variabili d'Ambiente (Opzionale)

Modificare i file `.env` secondo le proprie esigenze. Le configurazioni di default funzionano out-of-the-box.

**⚠️ IMPORTANTE**: Cambiare il `JWT_SECRET` in produzione!

## 🎯 Avvio del Progetto

### Avvio Completo con Docker Compose

```bash
docker-compose up --build
```

I servizi saranno disponibili su:

- **Frontend (CityFixUI)**: http://localhost:5173
- **API Gateway (Orchestrator)**: http://localhost:8000
- **AuthService**: http://localhost:8001
- **AdminService**: http://localhost:8002
- **TicketService**: http://localhost:8003
- **MediaService**: http://localhost:8004
- **GeoService**: http://localhost:8005
- **NotificationService**: http://localhost:8006
- **MongoDB**: http://localhost:27017

### Avvio in Background

```bash
docker-compose up -d
```

### Visualizzare i Log

```bash
# Tutti i servizi
docker-compose logs -f

# Servizio specifico
docker-compose logs -f frontend
docker-compose logs -f orchestrator
```

### Fermare i Servizi

```bash
docker-compose down
```

### Rimuovere anche i Volumi

```bash
docker-compose down -v
```

## 📁 Struttura del Progetto

```
cityfix/
├── src/
│   ├── CityFixUI/              # Frontend React
│   │   ├── src/
│   │   │   ├── components/     # Componenti React
│   │   │   ├── pages/          # Pagine applicazione
│   │   │   ├── hooks/          # Custom hooks
│   │   │   ├── services/       # API client
│   │   │   ├── store/          # State management (Context)
│   │   │   ├── types/          # TypeScript interfaces
│   │   │   ├── App.tsx
│   │   │   └── main.tsx
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   └── Dockerfile
│   │
│   ├── Orchestrator/           # API Gateway
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── admin.py
│   │   │   ├── tickets.py
│   │   │   ├── media.py
│   │   │   ├── geo.py
│   │   │   └── notifications.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── middleware.py
│   │   └── Dockerfile
│   │
│   ├── AuthService/            # Autenticazione
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── Dockerfile
│   │
│   ├── AdminService/           # Amministrazione
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── Dockerfile
│   │
│   ├── TicketService/          # Gestione ticket
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── Dockerfile
│   │
│   ├── MediaService/           # Upload/download media
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── Dockerfile
│   │
│   ├── GeoService/             # Geolocalizzazione
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── database.py
│   │   └── Dockerfile
│   │
│   └── NotificationService/    # Notifiche
│       ├── main.py
│       ├── routes.py
│       ├── models.py
│       ├── database.py
│       └── Dockerfile
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🔧 Servizi

### AuthService (porta 8001)
Gestisce autenticazione e autorizzazione degli utenti.

**Endpoints:**
- `POST /auth/register` - Registrazione nuovo utente
- `POST /auth/login` - Login (ritorna JWT token)
- `GET /auth/me` - Info utente corrente
- `POST /auth/logout` - Logout

### AdminService (porta 8002)
Gestisce funzionalità amministrative.

**Endpoints:**
- `GET /admin/municipalities` - Lista municipalità
- `POST /admin/municipalities` - Crea municipalità
- `GET /admin/stats` - Statistiche aggregate
- `GET /admin/tickets/all` - Tutti i ticket

### TicketService (porta 8003)
Gestisce le segnalazioni (ticket).

**Endpoints:**
- `POST /tickets/create` - Crea nuovo ticket
- `GET /tickets/list` - Lista ticket (filtrabili)
- `GET /tickets/{ticket_id}` - Dettagli ticket
- `PATCH /tickets/{ticket_id}` - Aggiorna ticket
- `POST /tickets/{ticket_id}/comments` - Aggiungi commento
- `POST /tickets/{ticket_id}/feedback` - Aggiungi feedback

### MediaService (porta 8004)
Gestisce upload e download di file multimediali.

**Endpoints:**
- `POST /media/upload` - Upload file
- `GET /media/{file_id}` - Download file
- `DELETE /media/{file_id}` - Elimina file

### GeoService (porta 8005)
Gestisce geolocalizzazione e mappe.

**Endpoints:**
- `POST /geo/geocode` - Converti indirizzo in coordinate
- `POST /geo/reverse-geocode` - Converti coordinate in indirizzo
- `GET /geo/map/tiles` - Info tile map OpenStreetMap
- `GET /geo/boundaries` - Confini municipalità

### NotificationService (porta 8006)
Gestisce notifiche agli utenti.

**Endpoints:**
- `POST /notify/send` - Invia notifica
- `GET /notify/user/{user_id}` - Notifiche utente
- `PATCH /notify/{notification_id}/read` - Marca come letta

## 🗄️ Schema Database

### Collection: users
```javascript
{
  _id: ObjectId,
  email: String,
  password_hash: String,
  role: String, // "citizen" | "operator" | "admin"
  tenant_id: String,
  created_at: DateTime
}
```

### Collection: municipalities
```javascript
{
  _id: ObjectId,
  name: String,
  location: {
    lat: Number,
    lon: Number,
    address: String
  },
  admin_id: String,
  created_at: DateTime
}
```

### Collection: tickets
```javascript
{
  _id: ObjectId,
  title: String,
  description: String,
  location: {
    lat: Number,
    lon: Number,
    address: String
  },
  status: String, // "pending" | "in_progress" | "completed" | "rejected"
  category: String,
  reported_by: String,
  assigned_to: String,
  images: [String],
  tenant_id: String,
  comments: [{
    user_id: String,
    message: String,
    created_at: DateTime
  }],
  feedback: {
    rating: Number,
    comment: String,
    created_at: DateTime
  },
  created_at: DateTime,
  updated_at: DateTime
}
```

### Collection: media
```javascript
{
  _id: ObjectId,
  file_id: String,
  filename: String,
  stored_filename: String,
  url: String,
  ticket_id: String,
  uploaded_by: String,
  size: Number,
  content_type: String,
  created_at: DateTime
}
```

### Collection: operators
```javascript
{
  _id: ObjectId,
  name: String,
  tenant_id: String,
  categories: [String],
  created_at: DateTime
}
```

### Collection: notifications
```javascript
{
  _id: ObjectId,
  user_id: String,
  message: String,
  type: String, // "info" | "warning" | "success" | "error"
  ticket_id: String,
  read: Boolean,
  created_at: DateTime
}
```

## 📚 API Documentation

Ogni servizio FastAPI espone la documentazione interattiva Swagger UI:

- **Orchestrator**: http://localhost:8000/docs
- **AuthService**: http://localhost:8001/docs
- **AdminService**: http://localhost:8002/docs
- **TicketService**: http://localhost:8003/docs
- **MediaService**: http://localhost:8004/docs
- **GeoService**: http://localhost:8005/docs
- **NotificationService**: http://localhost:8006/docs

## 🔐 Autenticazione

Il sistema usa JWT (JSON Web Tokens) per l'autenticazione.

**Flow:**
1. L'utente fa login tramite `POST /auth/login`
2. Il server ritorna un JWT token
3. Il token viene salvato nel localStorage del browser
4. Ogni richiesta include il token nell'header: `Authorization: Bearer <token>`
5. I servizi validano il token prima di processare le richieste

## 🌍 Connessione MongoDB

Per connettersi al database MongoDB con MongoDB Compass:

```
mongodb://admin:admin123@localhost:27017/cityfix?authSource=admin
```

## 🧪 Testing

### Test degli Endpoint

Usare Swagger UI (vedi sezione API Documentation) oppure tools come:
- **Postman**
- **Insomnia**
- **curl**

Esempio con curl:

```bash
# Registrazione
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","role":"citizen"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

## 🐛 Troubleshooting

### Porta già in uso
Se una porta è già occupata, modificare le porte nel `docker-compose.yml`

### MongoDB non si connette
Verificare che il container MongoDB sia running:
```bash
docker-compose ps
```

### Frontend non raggiunge il backend
Verificare le variabili d'ambiente in `.env` del frontend e che l'Orchestrator sia running.

### Hot Reload non funziona
I volumi sono configurati per il hot reload. Verificare i mount volumes nel `docker-compose.yml`.

## 🚦 Sviluppo Locale (senza Docker)

### Backend

Ogni servizio può essere avviato localmente:

```bash
cd src/AuthService
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### Frontend

```bash
cd src/CityFixUI
npm install
npm run dev
```

## 📝 Note

- I servizi usano `--reload` in development per hot reloading
- Le password sono hashate con bcrypt
- I token JWT scadono dopo 24 ore (configurabile)
- Le immagini caricate sono salvate nel volume Docker persistente
- OpenStreetMap viene usato per le mappe (nessuna API key richiesta)

## 🤝 Contribuire

Per contribuire al progetto:

1. Fork del repository
2. Crea un branch per la feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è distribuito con licenza MIT.

## 👥 Autori

Gruppo 9:
Borrelli Simone
De Maio Michele
Riccardi Simone

## 🙏 Ringraziamenti

- FastAPI community
- React community
- OpenStreetMap contributors