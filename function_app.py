import azure.functions as func
import json
import os
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient
import re

# Initialize the function app
app = func.FunctionApp()

# Helper function: Sanitize student name for blob file naming
def sanitize_name(student_name: str) -> str:
    """
    Convert student name to sanitized format (lowercase, replace spaces/special chars with hyphens).
    Example: "Alice Patel" -> "alice-patel"
    """
    sanitized = student_name.lower().strip()
    sanitized = re.sub(r'[^\w\-]', '-', sanitized)
    sanitized = re.sub(r'-+', '-', sanitized)
    sanitized = sanitized.strip('-')
    return sanitized

# Helper function: Generate blob file name with timestamp
def create_blob_name(student_name: str, submission_date: str) -> str:
    """
    Create blob file name from student name and submission date.
    Format: sanitized-name_yyyyMMddTHHmmssZ.json
    Example: "alice-patel_20260705T103000Z.json"
    """
    try:
        dt = datetime.fromisoformat(submission_date.replace('Z', '+00:00'))
        timestamp = dt.strftime('%Y%m%dT%H%M%S') + 'Z'
        sanitized = sanitize_name(student_name)
        return f"{sanitized}_{timestamp}.json"
    except ValueError:
        return None

# HTTP POST trigger function
@app.route(route="submitProject", methods=["POST"])
def submit_project(req: func.HttpRequest) -> func.HttpResponse:
    """
    Accept student project submission, validate, and store in Azure Blob Storage.
    """
    try:
        # Parse JSON body
        try:
            submission_data = req.get_json()
        except ValueError:
            return func.HttpResponse(
                json.dumps({"status": "error", "message": "Invalid JSON format"}),
                status_code=400,
                mimetype="application/json"
            )

        # Define required and optional fields
        required_fields = ['studentName', 'email', 'projectTitle', 'technology', 'submissionDate']
        optional_fields = ['comments']

        # Validate required fields
        missing_fields = [field for field in required_fields if field not in submission_data or not submission_data[field]]
        if missing_fields:
            return func.HttpResponse(
                json.dumps({"status": "error", "message": "Missing required fields", "missing_fields": missing_fields}),
                status_code=400,
                mimetype="application/json"
            )

        # Build output JSON with all fields + metadata
        output_json = {
            "studentName": submission_data.get("studentName", ""),
            "email": submission_data.get("email", ""),
            "projectTitle": submission_data.get("projectTitle", ""),
            "technology": submission_data.get("technology", ""),
            "submissionDate": submission_data.get("submissionDate", ""),
            "comments": submission_data.get("comments", ""),
            "receivedAtUtc": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "source": "azure-function-http-trigger"
        }

        # Generate blob file name
        blob_name = create_blob_name(output_json["studentName"], output_json["submissionDate"])
        if not blob_name:
            return func.HttpResponse(
                json.dumps({"status": "error", "message": "Invalid submission date format"}),
                status_code=400,
                mimetype="application/json"
            )

        # Get configuration from environment variables
        storage_connection_string = os.environ.get("STORAGE_CONNECTION_STRING")
        blob_container_name = os.environ.get("BLOB_CONTAINER_NAME", "project-submissions")

        if not storage_connection_string:
            return func.HttpResponse(
                json.dumps({"status": "error", "message": "Storage configuration unavailable"}),
                status_code=500,
                mimetype="application/json"
            )

        # Upload to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        container_client = blob_service_client.get_container_client(blob_container_name)
        container_client.upload_blob(blob_name, json.dumps(output_json))

        # Return success response
        return func.HttpResponse(
            json.dumps({
                "status": "success",
                "message": "Submission logged successfully",
                "blobName": blob_name,
                "containerName": blob_container_name
            }),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        # Log error securely (do not expose connection strings or internal details)
        return func.HttpResponse(
            json.dumps({"status": "error", "message": "An error occurred processing your submission"}),
            status_code=500,
            mimetype="application/json"
        )
