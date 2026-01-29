# Contribuire a CityFix

Grazie per il tuo interesse nel contribuire a CityFix! Seguendo queste linee guida aiuterai a mantenere il progetto organizzato e di qualità.

## 📋 Come Contribuire

### 1. Fork e Clone

1. Fai un fork del repository
2. Clona il tuo fork localmente:
   ```bash
   git clone https://github.com/tuo-username/cityfix.git
   cd cityfix
   ```

### 2. Crea un Branch

Crea un branch per la tua feature o bug fix:

```bash
git checkout -b feature/nome-feature
# oppure
git checkout -b fix/nome-bug
```

### 3. Sviluppa

- Scrivi codice pulito e ben documentato
- Segui le convenzioni di stile del progetto
- Aggiungi test se necessario
- Testa le tue modifiche localmente

### 4. Commit

Usa commit messages descrittivi:

```bash
git commit -m "feat: aggiungi notifiche push"
git commit -m "fix: risolvi problema upload immagini"
git commit -m "docs: aggiorna README"
```

Convenzioni per i commit:
- `feat:` - Nuova feature
- `fix:` - Bug fix
- `docs:` - Documentazione
- `style:` - Formattazione
- `refactor:` - Refactoring del codice
- `test:` - Aggiunta test
- `chore:` - Manutenzione

### 5. Push e Pull Request

```bash
git push origin feature/nome-feature
```

Apri una Pull Request su GitHub con:
- Titolo descrittivo
- Descrizione dettagliata delle modifiche
- Screenshot se applicabile
- Reference a issue correlate

## 🎨 Code Style

### Python (Backend)

- Usa **PEP 8** per lo stile del codice
- Type hints quando possibile
- Docstrings per funzioni pubbliche
- Max 88 caratteri per linea (Black formatter)

### TypeScript/React (Frontend)

- Usa **ESLint** e **Prettier**
- Componenti funzionali con hooks
- TypeScript strict mode
- Props ben tipizzate

## 🧪 Testing

- Testa le modifiche localmente prima del commit
- Assicurati che tutti i servizi si avviino correttamente
- Verifica che le API rispondano come previsto

## 📝 Documentazione

- Aggiorna il README se aggiungi nuove features
- Commenta il codice complesso
- Aggiorna gli esempi se necessario

## ❓ Domande

Se hai domande, apri una issue con il tag `question`.

## 📜 Licenza

Contribuendo, accetti che il tuo codice sarà rilasciato sotto la licenza MIT del progetto.