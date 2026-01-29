# CityFix Postman Collection

Complete API testing collection for the CityFix platform.

## Contents

- `CityFix-API.postman_collection.json` - API request collection
- `CityFix-Environment.postman_environment.json` - Environment variables

## Quick Start

### 1. Import Collection

1. Open Postman
2. Click "Import" button
3. Select `CityFix-API.postman_collection.json`
4. Collection will appear in your sidebar

### 2. Import Environment

1. Click "Import" button
2. Select `CityFix-Environment.postman_environment.json`
3. Select "CityFix Environment" from environment dropdown

### 3. Configure Environment

Update these variables in the environment:

- `base_url` - Your API URL (default: http://localhost:8000)
- `user_email` - Test user email
- `user_password` - Test user password
- `municipality_id` - Your municipality ID

### 4. Run Requests

The collection is organized by service:

1. **Auth Service** - Start here to authenticate
2. **Ticket Service** - Create and manage tickets
3. **Admin Service** - Administrative operations
4. **Media Service** - File uploads
5. **Geo Service** - Geocoding operations
6. **Notification Service** - User notifications

## Authentication Flow

1. **Register** (optional): Create a new user account
2. **Login**: Get JWT token (automatically saved to `api_token`)
3. All subsequent requests use the token automatically

The collection uses Bearer token authentication with the `api_token` variable.

## Environment Variables

### Automatically Set

These are set by test scripts:

- `api_token` - JWT access token (from login)
- `user_id` - Current user ID (from login)
- `ticket_id` - Last created ticket ID

### Manually Set

- `base_url` - API base URL
- `user_email` - User email for login
- `user_password` - User password
- `municipality_id` - Municipality identifier

## Request Organization

### Auth Service

- `POST /auth/register` - Create new user
- `POST /auth/login` - Authenticate and get token
- `GET /auth/me` - Get current user info

### Ticket Service

- `POST /tickets/create` - Create new ticket
- `GET /tickets/list` - List tickets with filters
- `GET /tickets/:id` - Get ticket details
- `PUT /tickets/:id/status` - Update ticket status
- `PUT /tickets/:id/assign` - Assign ticket to operator
- `POST /tickets/:id/comments` - Add comment
- `POST /tickets/:id/feedback` - Add feedback/rating

### Admin Service

- `GET /admin/stats` - Get platform statistics
- `GET /admin/municipalities` - List all municipalities
- `POST /admin/municipalities` - Create municipality
- `GET /admin/municipalities/stats` - Get per-municipality stats

### Media Service

- `POST /media/upload` - Upload file (multipart/form-data)
- `GET /media/:id` - Download file

### Geo Service

- `GET /geo/geocode` - Convert address to coordinates
- `GET /geo/reverse` - Convert coordinates to address

### Notification Service

- `POST /notifications/create` - Create notification
- `GET /notifications/user/:id` - Get user notifications
- `PUT /notifications/:id/read` - Mark as read
- `DELETE /notifications/:id` - Delete notification

## Test Scripts

The collection includes test scripts that:

- Automatically save authentication tokens
- Extract and save IDs from responses
- Validate response status codes
- Set environment variables for chaining requests

### Example: Login Flow

```javascript
// Login request test script
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set('api_token', jsonData.access_token);
    pm.environment.set('user_id', jsonData.user.id);
}
```

## Running Collection

### Run Entire Collection

1. Click "..." next to collection name
2. Select "Run collection"
3. Choose environment
4. Click "Run CityFix API"

### Run Folder

1. Right-click on a folder (e.g., "Ticket Service")
2. Select "Run folder"

### Run Single Request

Click "Send" button on any request

## Example Workflows

### Workflow 1: Create and Manage Ticket

1. Auth Service → Login
2. Ticket Service → Create Ticket
3. Ticket Service → Get Ticket by ID
4. Ticket Service → Add Comment
5. Ticket Service → Update Ticket Status

### Workflow 2: Operator Assignment

1. Auth Service → Login (as admin/operator)
2. Ticket Service → List Tickets (pending)
3. Ticket Service → Assign Ticket
4. Ticket Service → Update Ticket Status (in_progress)
5. Ticket Service → Add Comment (report)

### Workflow 3: Complete Ticket with Feedback

1. Ticket Service → Update Ticket Status (completed)
2. Ticket Service → Add Feedback

## Environments

You can create multiple environments for different setups:

### Local Development

```json
{
  "base_url": "http://localhost:8000"
}
```

### Staging

```json
{
  "base_url": "https://api-staging.cityfix.example.com"
}
```

### Production

```json
{
  "base_url": "https://api.cityfix.example.com"
}
```

## File Upload

The Media Service → Upload File request uses `multipart/form-data`:

1. Select request
2. Go to "Body" tab
3. Select file for `file` field
4. `ticket_id` is auto-filled from environment

## Tips and Tricks

### Quick Test

Create a test suite that runs:
1. Register → Login → Create Ticket → List Tickets

### Save Responses

Use "Save Response" to keep examples for documentation

### Share Collection

Export collection with examples:
1. Right-click collection
2. Export
3. Share the JSON file

### Newman CLI

Run collection from command line:

```bash
npm install -g newman

newman run CityFix-API.postman_collection.json \
  -e CityFix-Environment.postman_environment.json \
  --reporters cli,json
```

## Troubleshooting

### Token Expired

Run Auth Service → Login again

### Invalid Environment Variable

Check environment is selected and variables are set

### Connection Error

Verify `base_url` and ensure services are running:

```bash
docker-compose ps
curl http://localhost:8000/health
```

### Request Failing

Check:
1. Authentication token is valid
2. Required IDs are set (ticket_id, user_id)
3. Request body format matches API expectations

## API Documentation

Each service also provides Swagger/OpenAPI docs:

- Auth: http://localhost:8001/docs
- Admin: http://localhost:8002/docs
- Ticket: http://localhost:8003/docs
- Media: http://localhost:8004/docs
- Geo: http://localhost:8005/docs
- Notification: http://localhost:8006/docs
- Orchestrator: http://localhost:8000/docs

## Contributing

To add new requests:

1. Add request to appropriate folder
2. Add test scripts to extract IDs
3. Use environment variables for dynamic values
4. Document in this README

## Support

For issues:
- Check service logs: `docker-compose logs <service-name>`
- Verify service health: http://localhost:8000/health
- Review API docs at /docs endpoints
