# Setup Guide

## Prerequisites

- Azure Subscription
- Azure CLI or Azure Portal access
- Python 3.9+ (for local development)
- Git

## Step-by-Step Setup

### 1. Create Azure Resource Group

```bash
az group create --name rg-student-submissions --location eastus
```

### 2. Create Storage Account

```bash
az storage account create \
  --name stgstudentsubmissions \
  --resource-group rg-student-submissions \
  --location eastus \
  --sku Standard_LRS
```

Replace `stgstudentsubmissions` with a globally unique name (lowercase, 3-24 characters).

### 3. Create Blob Container

```bash
az storage container create \
  --name project-submissions \
  --account-name stgstudentsubmissions \
  --public-access off
```

### 4. Get Storage Connection String

```bash
az storage account show-connection-string \
  --name stgstudentsubmissions \
  --resource-group rg-student-submissions \
  --query connectionString -o tsv
```

Copy this connection string—you'll need it in the next step.

### 5. Create Azure Function App

```bash
az functionapp create \
  --name func-student-submissions \
  --storage-account stgstudentsubmissions \
  --consumption-plan-location eastus \
  --resource-group rg-student-submissions \
  --runtime python \
  --runtime-version 3.11
```

Replace function name if `func-student-submissions` is taken.

### 6. Configure Application Settings

Set environment variables in the Function App:

```bash
az functionapp config appsettings set \
  --name func-student-submissions \
  --resource-group rg-student-submissions \
  --settings \
	STORAGE_CONNECTION_STRING="<paste-connection-string-from-step-4>" \
	BLOB_CONTAINER_NAME="project-submissions"
```

### 7. Deploy Function Code

**Option A: Deploy from GitHub**

Deploy directly from this repository using the Azure Portal or Azure CLI.

**Option B: Deploy with Local Tools**

```bash
pip install -r requirements.txt
func azure functionapp publish func-student-submissions --build remote
```

### 8. Get Function URL

```bash
az functionapp function show \
  --name func-student-submissions \
  --resource-group rg-student-submissions \
  --function-name submitProject \
  --query invokeUrlTemplate -o tsv
```

The URL will look like:
```
https://func-student-submissions.azurewebsites.net/api/submitProject?code=XXXXXX
```

### 9. Test the Endpoint

See `docs/testing-guide.md` for testing instructions.

## Verify Blob Storage

1. Go to Azure Portal
2. Navigate to your Storage Account
3. Click "Containers" → "project-submissions"
4. After testing, you should see JSON files with names like:
   - alice-patel_20260705T103000Z.json
   - john-smith_20260705T103100Z.json

## Local Development (Optional)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp local.settings.json.example local.settings.json
# Edit local.settings.json with your connection string
func start
```

Then test locally at:
```
http://localhost:7071/api/submitProject
```

## Troubleshooting

**Function won't deploy:**
- Check function name is globally unique
- Verify storage account permissions
- Run: `func azure functionapp publish func-student-submissions --build remote`

**Connection string errors:**
- Verify `STORAGE_CONNECTION_STRING` is set in Application Settings
- Check it doesn't contain quotes or extra whitespace

**Upload fails:**
- Confirm container name matches `BLOB_CONTAINER_NAME` setting
- Check storage account network settings (should allow Function App access)

## Cleanup

To avoid charges after completing the demo:

```bash
az group delete --name rg-student-submissions --yes
```
