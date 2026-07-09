# Testing Guide

## Test Setup

Before testing, ensure you have:
- Function URL (from setup guide step 8)
- Sample payload in `sample-payload/sample-request.json`
- Tool: curl, Postman, Thunder Client, or VS Code REST Client

## Test with cURL

### Test Valid Submission

```bash
curl -X POST "YOUR_FUNCTION_URL_HERE" \
  -H "Content-Type: application/json" \
  -d @sample-payload/sample-request.json
```

**Expected Response (HTTP 200):**
```json
{
  "status": "success",
  "message": "Submission logged successfully",
  "blobName": "alice-patel_20260705T103000Z.json",
  "containerName": "project-submissions"
}
```

### Test Missing Required Field

```bash
curl -X POST "YOUR_FUNCTION_URL_HERE" \
  -H "Content-Type: application/json" \
  -d '{"studentName": "Bob", "email": "bob@example.com"}'
```

**Expected Response (HTTP 400):**
```json
{
  "status": "error",
  "message": "Missing required fields",
  "missing_fields": ["projectTitle", "technology", "submissionDate"]
}
```

### Test Invalid JSON

```bash
curl -X POST "YOUR_FUNCTION_URL_HERE" \
  -H "Content-Type: application/json" \
  -d '{invalid json'
```

**Expected Response (HTTP 400):**
```json
{
  "status": "error",
  "message": "Invalid JSON format"
}
```

## Test with Postman

1. Open Postman
2. Create new POST request
3. Enter URL: `YOUR_FUNCTION_URL_HERE`
4. Set Header: `Content-Type: application/json`
5. Go to Body tab → Raw → JSON
6. Paste sample payload from `sample-payload/sample-request.json`
7. Click Send
8. View response in Response panel

## Test with Thunder Client (VS Code)

1. Install Thunder Client extension
2. Create new request
3. Method: POST
4. URL: `YOUR_FUNCTION_URL_HERE`
5. Headers: `Content-Type: application/json`
6. Body: Paste sample payload
7. Send
8. Check response

## Test with VS Code REST Client

1. Create file: `test.http`
2. Add:
```http
POST YOUR_FUNCTION_URL_HERE
Content-Type: application/json

{
  "studentName": "Alice Patel",
  "email": "alice@example.com",
  "projectTitle": "Azure Serverless Logger",
  "technology": "Azure Functions, Blob Storage",
  "submissionDate": "2026-07-05T10:30:00Z",
  "comments": "Portfolio project"
}
```
3. Click "Send Request" above the POST line
4. View response in output panel

## Verify Blob Storage

1. Go to Azure Portal
2. Navigate to Storage Account: `stgstudentsubmissions` (or your name)
3. Click Containers → `project-submissions`
4. You should see JSON files named like:
   - `alice-patel_20260705T103000Z.json`
   - `john-smith_20260706T140000Z.json`
5. Click a file to view its contents (should match your submission + metadata)

## Test Cases Checklist

- [ ] Valid submission returns HTTP 200
- [ ] Invalid JSON returns HTTP 400
- [ ] Missing required field returns HTTP 400 with field list
- [ ] Blob file created in storage (visible in Portal)
- [ ] Blob file name follows format: sanitized-name_yyyyMMddTHHmmssZ.json
- [ ] Blob file contains receivedAtUtc timestamp
- [ ] Blob file contains source="azure-function-http-trigger"
- [ ] Comments field preserved if provided
- [ ] Comments field empty string if not provided
- [ ] Error messages do not expose connection strings

## Troubleshooting

**HTTP 401 - Unauthorized:**
- Check function URL includes `code=` parameter
- Verify you copied the full URL from Azure Portal

**HTTP 500 - Internal Server Error:**
- Check STORAGE_CONNECTION_STRING is set in Application Settings
- Verify connection string is not wrapped in quotes
- Check blob container exists and is named exactly: `project-submissions`

**Blob file not appearing:**
- Verify HTTP 200 response received
- Check storage account in Portal → Containers
- Wait a few seconds and refresh
- Check connection string validity

**Wrong blob file name:**
- Verify submissionDate is ISO 8601 format (e.g., "2026-07-05T10:30:00Z")
- Check studentName is being sanitized (spaces → hyphens, lowercase)
