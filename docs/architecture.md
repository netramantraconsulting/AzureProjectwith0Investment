# Architecture

## System Overview

```
User / Form / Postman
		|
		| HTTP POST JSON
		v
Azure Function HTTP Trigger
		|
		| Validate + transform payload
		v
Azure Blob Storage Container
		|
		| JSON file saved
		v
GitHub Portfolio Evidence
```

## Component Descriptions

### 1. Client (User / Form / Postman)
- Sends HTTP POST request to Azure Function URL
- Includes JSON payload with student submission data
- Receives JSON success/error response

### 2. Azure Function HTTP Trigger
- Python runtime function
- Validates JSON format
- Checks required fields (studentName, email, projectTitle, technology, submissionDate)
- Adds metadata:
  - receivedAtUtc: Current UTC timestamp
  - source: "azure-function-http-trigger"
- Sanitizes student name for file naming
- Returns structured JSON response

### 3. Azure Blob Storage
- Stores submission JSON files
- Container name: "project-submissions"
- File naming: sanitized-name_yyyyMMddTHHmmssZ.json
- Private container (no public access)
- Connection via environment-based credentials

### 4. Portfolio Evidence
- Blob files serve as audit trail
- GitHub repository demonstrates serverless architecture
- Code samples for portfolio/interview discussions

## Data Flow

1. JSON POST → Function parses and validates
2. If invalid → HTTP 400 error response
3. If valid → Add timestamp + source metadata
4. Upload JSON to blob with sanitized filename
5. Return HTTP 200 success with blob name
6. Client receives confirmation

## Error Handling

| Scenario | HTTP Status | Response |
|----------|-------------|----------|
| Invalid JSON | 400 | `{"status": "error", "message": "Invalid JSON format"}` |
| Missing required field | 400 | `{"status": "error", "message": "Missing required fields", "missing_fields": [...]}` |
| Invalid date format | 400 | `{"status": "error", "message": "Invalid submission date format"}` |
| Storage connection error | 500 | `{"status": "error", "message": "Storage configuration unavailable"}` |
| Unexpected error | 500 | `{"status": "error", "message": "An error occurred processing your submission"}` |

No secrets or internal details are exposed in error messages.
