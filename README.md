# Student Project Submission Logger

A beginner-friendly serverless Azure solution demonstrating cloud-native REST API design. This project showcases how to build, deploy, and secure an HTTP-triggered Azure Function that validates student project submissions and stores them in Azure Blob Storage.

## Overview

**Student Project Submission Logger** is a complete, production-ready example of a serverless submission system built for Azure beginners preparing for AZ-900 or PL-900 certifications.

The solution exposes an HTTP endpoint where users submit project details in JSON format. The Azure Function:
- Validates incoming JSON structure and required fields
- Transforms the payload with server-side timestamps and metadata
- Generates a sanitized blob filename from student name and submission date
- Uploads the enriched JSON document to Azure Blob Storage
- Returns a structured success or error response

This project demonstrates enterprise patterns in serverless architecture, making it ideal for building portfolio evidence and interview discussions.

## Business Scenario

Educational platforms, bootcamps, training organizations, and self-directed learning communities need simple, scalable mechanisms for capturing and archiving project submissions.

Instead of managing spreadsheets or email threads, this API-first solution provides:
- **Immediate data persistence** – Each submission is immediately stored with an immutable timestamp
- **Audit trail** – Every submission creates a dated blob file for compliance and review
- **Scalability** – Serverless architecture handles traffic spikes without infrastructure management
- **Developer experience** – Simple JSON API requiring no authentication complexity for basic usage

## Architecture

```
┌─────────────────────┐
│  User / Client      │
│ (Postman, Form, etc)│
└──────────┬──────────┘
           │
           │ HTTP POST (JSON)
           │
           ▼
┌──────────────────────────────────┐
│   Azure Function HTTP Trigger    │
│  ✓ Validate JSON                 │
│  ✓ Check required fields         │
│  ✓ Add timestamps & metadata     │
│  ✓ Sanitize filename             │
└──────────┬───────────────────────┘
           │
           │ Upload blob
           │
           ▼
┌──────────────────────────────────┐
│ Azure Blob Storage (Container)   │
│ project-submissions/             │
│ ├─ alice-patel_20260705T..Z.json │
│ ├─ john-smith_20260705T..Z.json  │
│ └─ ...                           │
└──────────────────────────────────┘
           │
           │
           ▼
┌──────────────────────────────────┐
│  Portfolio Evidence & Audit Trail│
│  (GitHub Repo + Blob Artifacts)  │
└──────────────────────────────────┘
```

## Solution Flow

1. **Client sends HTTP POST** with JSON payload containing studentName, email, projectTitle, technology, submissionDate, and optional comments
2. **Function receives request** and parses JSON
3. **Validation layer** checks JSON format and required fields
4. **Transform layer** adds `receivedAtUtc` timestamp (server-generated) and `source` metadata
5. **Sanitizer function** converts "Alice Patel" → "alice-patel" for safe blob naming
6. **Blob upload** stores JSON file as `alice-patel_20260705T103000Z.json`
7. **Success response** returns HTTP 200 with blob name and container name
8. **Error responses** return HTTP 400 (validation) or HTTP 500 (server error) with safe error messages

## Features

- ✅ **HTTP POST endpoint** – Simple REST interface for submissions
- ✅ **JSON validation** – Enforces required fields before processing
- ✅ **Server-side timestamps** – Adds `receivedAtUtc` (UTC ISO 8601 format)
- ✅ **Metadata enrichment** – Includes source: "azure-function-http-trigger"
- ✅ **Sanitized blob naming** – Supports special characters in student names safely
- ✅ **Azure Blob Storage integration** – Uses official Azure Storage SDK
- ✅ **Environment-based configuration** – No hardcoded secrets in code
- ✅ **Comprehensive error handling** – Returns safe, user-friendly error messages
- ✅ **Local development ready** – Includes example settings file for local testing
- ✅ **Production-grade documentation** – Setup, testing, architecture, and cost guides

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.11+ |
| **Compute** | Azure Functions (Consumption Plan) |
| **Storage** | Azure Blob Storage |
| **SDK** | Azure Functions Python model, Azure Storage Blob SDK |
| **Configuration** | Environment variables (no .env committed) |
| **API Protocol** | HTTP/REST with JSON |
| **Version Control** | Git / GitHub |

## Project Structure

```
student-project-submission-logger/
├─ README.md                           # This file
├─ function_app.py                     # Azure Function main code
├─ requirements.txt                    # Python dependencies
├─ host.json                           # Azure Functions host config
├─ local.settings.json.example         # Template for local development
├─ .env.example                        # Environment variables template
├─ .gitignore                          # Excludes secrets & artifacts
│
├─ docs/
│  ├─ architecture.md                  # Detailed system design
│  ├─ setup-guide.md                   # Step-by-step Azure setup
│  ├─ testing-guide.md                 # Testing with curl, Postman, Thunder Client
│  └─ cost-note.md                     # Cost disclaimers & budget guidance
│
├─ sample-payload/
│  └─ sample-request.json              # Example submission JSON
│
├─ screenshots/                        # Portfolio evidence screenshots
│  └─ .gitkeep
│
└─ LICENSE                             # MIT License
```

## Prerequisites

- **Azure Subscription** – Free tier eligible ($200 credit for 30 days or 1M free Function executions/month)
- **Azure CLI** – [Download here](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- **Python 3.9+** – [Download here](https://www.python.org/)
- **Git** – [Download here](https://git-scm.com/)
- **Text editor or IDE** – VS Code (free), Visual Studio, PyCharm
- **curl, Postman, or Thunder Client** – For API testing

## Azure Resources Required

To deploy this solution, you will create:

| Resource | Purpose | Free Tier Eligible |
|----------|---------|-------------------|
| **Resource Group** | Logical container for resources | Yes |
| **Storage Account** | Hosts blob container | Yes (5 GB) |
| **Blob Container** | Stores submission JSON files | Yes |
| **Function App** | Runs Python HTTP trigger | Yes (1M requests/month) |
| **Application Settings** | Stores secrets & config | Yes |

**Estimated Free Tier Cost:** €0 for demo usage (< 1000 requests, < 1 GB storage)

See `docs/cost-note.md` for full disclaimer.

## Local Development Setup

### 1. Clone the Repository

```sh
git clone https://github.com/netramantraconsulting/AzureProjectwith0Investment.git
cd student-project-submission-logger
```

### 2. Create Python Virtual Environment

```sh
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure Local Settings

```sh
cp local.settings.json.example local.settings.json

# Edit local.settings.json and add your STORAGE_CONNECTION_STRING
```

### 5. Run Locally

```sh
func start
```

Function will be available at: `http://localhost:7071/api/submitProject`

## Azure Deployment Overview

For complete deployment instructions, see `docs/setup-guide.md`.

**Quick Summary:**

```sh
# Create resource group
az group create --name rg-student-submissions --location eastus

# Create storage account (replace with globally unique name)
az storage account create --name stgstudentsubmissions \
  --resource-group rg-student-submissions --location eastus --sku Standard_LRS

# Create blob container
az storage container create --name project-submissions \
  --account-name stgstudentsubmissions --public-access off

# Create Function App
az functionapp create --name func-student-submissions \
  --storage-account stgstudentsubmissions \
  --consumption-plan-location eastus \
  --resource-group rg-student-submissions \
  --runtime python --runtime-version 3.11

# Deploy function
func azure functionapp publish func-student-submissions --build remote
```

## Configuration

### Environment Variables

The function reads configuration from Azure Application Settings (or local environment):

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `STORAGE_CONNECTION_STRING` | Yes | None | Connection to Azure Storage Account |
| `BLOB_CONTAINER_NAME` | No | project-submissions | Blob container name |

**Never commit actual connection strings to Git.** Use `local.settings.json.example` as a template.

### Setting Variables in Azure

```sh
az functionapp config appsettings set \
  --name func-student-submissions \
  --resource-group rg-student-submissions \
  --settings \
    STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;..." \
    BLOB_CONTAINER_NAME="project-submissions"
```

## Sample Request

**HTTP Method:** POST  
**Content-Type:** application/json

```json
{
  "studentName": "Alice Patel",
  "email": "alice@example.com",
  "projectTitle": "Azure Serverless Logger",
  "technology": "Azure Functions, Blob Storage",
  "submissionDate": "2026-07-05T10:30:00Z",
  "comments": "Portfolio project for AZ-900 preparation"
}
```

**Required fields:** studentName, email, projectTitle, technology, submissionDate  
**Optional fields:** comments

## Sample Response

**HTTP 200 – Success**

```json
{
  "status": "success",
  "message": "Submission logged successfully",
  "blobName": "alice-patel_20260705T103000Z.json",
  "containerName": "project-submissions"
}
```

**HTTP 400 – Validation Error (Missing Field)**

```json
{
  "status": "error",
  "message": "Missing required fields",
  "missing_fields": ["projectTitle", "submissionDate"]
}
```

**HTTP 400 – Invalid JSON**

```json
{
  "status": "error",
  "message": "Invalid JSON format"
}
```

**HTTP 500 – Server Error**

```json
{
  "status": "error",
  "message": "An error occurred processing your submission"
}
```

**Note:** Error messages are intentionally generic and safe. Connection strings, internal stack traces, and sensitive details are never exposed.

## Testing Guide

### Using curl

```sh
curl -X POST "YOUR_FUNCTION_URL_HERE" \
  -H "Content-Type: application/json" \
  -d @sample-payload/sample-request.json
```

### Using Postman

1. Create new POST request
2. Paste function URL
3. Headers tab: Add `Content-Type: application/json`
4. Body tab: Select "raw" and "JSON", paste sample payload
5. Click Send
6. Check response

### Using Thunder Client (VS Code)

1. Install Thunder Client extension
2. Create new request
3. Method: POST
4. URL: Paste function URL
5. Headers: `Content-Type: application/json`
6. Body: Paste sample payload
7. Send and verify response

### Verify Blob Storage

1. Open Azure Portal
2. Go to Storage Account → Containers → project-submissions
3. You should see JSON files: `alice-patel_20260705T103000Z.json`
4. Click file to view contents

See `docs/testing-guide.md` for comprehensive testing guidance.

## Security Considerations

### Code-Level Security

- ✅ **No hardcoded secrets** – All credentials read from environment variables
- ✅ **Input validation** – JSON and required field checks before processing
- ✅ **Safe error messages** – No stack traces or credential exposure in responses
- ✅ **Timestamp validation** – Submission date format checked before blob naming

### Deployment Security

- ✅ **Use Azure Application Settings** – Store secrets in Function App settings, not in code
- ✅ **Never commit secrets** – `.env` and `local.settings.json` listed in `.gitignore`
- ✅ **Private blob container** – No public access (public-access = off)
- ✅ **HTTPS only** – Azure Functions endpoint requires HTTPS by default
- ✅ **Managed by Azure** – No manual secret rotation needed for connection strings

### Best Practices

1. **Rotate connection strings periodically** (Azure Portal → Storage Account → Access Keys)
2. **Monitor Function App logs** for unusual activity
3. **Use Managed Identity** (future enhancement) to eliminate connection string secrets entirely
4. **Implement IP allow-listing** if Function App should only accept requests from specific networks
5. **Enable Application Insights** (future enhancement) for detailed logging and alerting

## Cost Considerations

### Free Tier Benefits

- **Azure Functions:** 1,000,000 free executions/month (Consumption Plan)
- **Azure Storage:** 5 GB free blob storage
- **Trial:** $200 credit for first 30 days
- **Always-free:** Function compute and storage within limits

### Estimation for Demo Usage

| Metric | Monthly Usage | Cost |
|--------|---------------|------|
| Function executions | 500 (< 1000) | €0 (free tier) |
| Blob storage | 10 MB | €0 (free tier) |
| **Total** | **Demo scale** | **€0** |

### Important Cost Disclaimers

⚠️ **Read Before Deployment:**

- **Azure pricing changes** – Verify current rates at [azure.microsoft.com/pricing](https://azure.microsoft.com/pricing/)
- **Free tier changes** – Microsoft periodically updates free tier limits
- **Trial expiration** – $200 credit expires after 30 days; pay-as-you-go begins unless disabled
- **Regional pricing** – Costs vary by Azure region
- **Set budget alerts** – Use Azure Portal Cost Management to alert on spending
- **Delete after demo** – Remove resource group when learning is complete

See `docs/cost-note.md` for detailed cost analysis.

## Learning Outcomes

By building and deploying this project, you will develop practical understanding of:

1. **Azure Functions**
   - HTTP-triggered functions
   - Python runtime model
   - Local and cloud execution
   - Consumption Plan economics

2. **Azure Blob Storage**
   - Container creation and management
   - Blob upload with SDK
   - Naming conventions
   - Access control and privacy

3. **Serverless Architecture**
   - Event-driven computing
   - Stateless function design
   - Cost optimization
   - Scalability without infrastructure

4. **REST API Development**
   - Request validation patterns
   - JSON schema design
   - HTTP status codes
   - Error response design

5. **Cloud Security Basics**
   - Secret management (environment variables)
   - Principle of least privilege (private containers)
   - Input validation
   - Safe error handling

6. **API Testing**
   - HTTP method usage (POST)
   - Content negotiation (JSON)
   - Testing tools (curl, Postman)
   - Response validation

7. **GitHub & Open Source Practices**
   - Professional README documentation
   - `.gitignore` for secrets management
   - Sample configurations and examples
   - Portfolio-quality code organization

## Future Enhancements

This project can be extended with:

- **Power Apps Front-End** – Build a canvas app for visual submission form without coding
- **Microsoft Dataverse** – Store submissions in Dataverse tables instead of blobs for advanced querying
- **Managed Identity** – Replace connection strings with Azure AD authentication token exchange
- **Application Insights** – Add distributed tracing, performance monitoring, and alert rules
- **GitHub Actions CI/CD** – Automate deployment to Azure on push to main branch
- **Power Automate Notifications** – Send email confirmation to student after submission

## Interview Discussion Points

### Opening Pitch

> "I built a serverless Student Project Submission Logger using Azure Functions and Blob Storage. The solution accepts JSON submissions via HTTP POST, validates required fields, enriches data with server-side timestamps, and stores each submission as a timestamped blob file. This demonstrates cloud-native API design, serverless compute, and secure Azure integrations."

### Key Talking Points

**Architecture & Design:**
- "I chose serverless architecture because submissions are event-driven and unpredictable in volume. No need to manage servers or pay for idle capacity."
- "The Function validates JSON at the entry point, preventing invalid data from reaching storage."
- "I sanitize student names when creating blob file names to handle special characters safely."

**Security & Best Practices:**
- "Connection strings are never hardcoded. They're stored as Azure Application Settings and read via `os.environ`."
- "Error messages are intentionally generic—they never expose connection strings or internal details."
- "The blob container is private (no public access), ensuring submissions are only accessible via authenticated storage calls."

**Scalability & Cost:**
- "Consumption Plan means I pay only for actual executions. No fixed infrastructure cost."
- "With 1 million free requests per month on Azure Functions, demo usage costs €0."
- "Each submission creates an immutable timestamped blob, providing an audit trail for compliance."

**Testing & Validation:**
- "I included sample payloads and testing guides using curl, Postman, and Thunder Client so anyone can verify the API."
- "Required field validation returns HTTP 400 with a list of missing fields for clear client feedback."
- "I tested locally using Azure Functions emulator before deploying to the cloud."

**GitHub Portfolio Value:**
- "This repository demonstrates professional README documentation, `.gitignore` security practices, and architectural thinking."
- "The setup guide is detailed enough for beginners; the code is clean and comment-friendly for recruiters to review."
- "This project is ideal for AZ-900 and PL-900 exam preparation because it touches core Azure services without overcomplication."

### Potential Follow-Up Questions & Answers

**Q: How would you secure this in production?**  
A: "I would implement Managed Identity to eliminate connection strings entirely. I'd enable Application Insights for logging and alerts, use Azure Key Vault for sensitive config, and implement IP allow-listing to restrict Function access to trusted networks."

**Q: How does the blob naming strategy work?**  
A: "Students names are sanitized to lowercase with spaces and special characters converted to hyphens (e.g., 'Alice Patel' → 'alice-patel'). The file name combines the sanitized name with a UTC timestamp from the submission date: alice-patel_20260705T103000Z.json. This ensures unique, sortable files without collisions."

**Q: Why add `receivedAtUtc` server-side instead of trusting the client?**  
A: "Clients can lie or have clock drift. The server generates the 'received' timestamp guarantees audit trail integrity and prevents backdating. The client's submission date is preserved separately for reporting purposes."

**Q: What happens if the blob upload fails?**  
A: "The function catches exceptions and returns HTTP 500 with a safe error message. The failure is logged, and the client knows the submission didn't persist. In production, I'd use Application Insights to alert ops teams."

**Q: How would you add authentication to prevent abuse?**  
A: "Azure Functions supports API keys by default. I could also integrate Azure AD for OAuth, or use Azure API Management to implement rate limiting and request signing."

## Screenshots

_Placeholder for portfolio evidence:_

- [ ] Postman request showing POST to Azure Function URL
- [ ] HTTP 200 success response with blob file name
- [ ] Azure Portal showing Storage Account blob container
- [ ] JSON blob file visible in Azure Portal
- [ ] Local development with `func start` running
- [ ] Azure Function App overview in Azure Portal
- [ ] VS Code with function code and debug session

_Add screenshots to the `screenshots/` directory and link them below when available._

## Contributing

This is a learning project. Contributions are welcome:

1. **Fork** the repository
2. **Create a feature branch:** `git checkout -b feature/your-enhancement`
3. **Make changes** and test locally with `func start`
4. **Commit:** `git commit -m "Add your feature"`
5. **Push:** `git push origin feature/your-enhancement`
6. **Open a Pull Request** with description of changes

Suggested contributions:
- Additional test cases or sample payloads
- Improvements to documentation
- Support for additional fields in submission model
- Example Power Apps front-end reference

## License

This project is licensed under the **MIT License**. See `LICENSE` file for full details.

**Summary:** You are free to use, modify, and distribute this project for personal, educational, and commercial purposes. No warranty is provided.

## Author

**Timir Das**  
Founder – Netra Mantra Consulting

- **GitHub:** [netramantraconsulting](https://github.com/netramantraconsulting)
- **YouTube:** [Technocrat Warriors](https://www.youtube.com/@technocratwarriors)

---

## Quick Links

- [Setup Guide](./docs/setup-guide.md) – Step-by-step Azure deployment
- [Testing Guide](./docs/testing-guide.md) – API testing with curl, Postman, Thunder Client
- [Architecture](./docs/architecture.md) – Detailed system design and data flow
- [Cost Note](./docs/cost-note.md) – Cost disclaimers and budget guidance
- [Sample Payload](./sample-payload/sample-request.json) – Example JSON submission

---

**Last Updated:** July 2026  
**Status:** Active & Maintained  
**Maintainer:** Timir Das
