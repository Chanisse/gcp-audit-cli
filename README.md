# GCP Audit CLI

A personal GCP auditing CLI tool for inspecting **IAM**, **project-level IAM bindings**, **GKE clusters**, **GCS buckets**, **Cloud Run**, **Cloud Functions**, and **Artifact Registry**.  

Designed for engineers who want a quick audit of their GCP projects using **Application Default Credentials** without exposing service account keys.

---

## Features

- Check overprivileged **custom service accounts** in a project
- Fetch **project-level IAM members** and split by users and service accounts
- Map **service accounts** to assigned roles
- Check **GKE clusters** for idle status
- Check **GCS buckets** for inactivity
- List **Cloud Run services** and show last deployment status
- List **Cloud Functions** in the project
- List **Artifact Registry repositories** and flag inactive ones

---

## Getting started

1. Clone
```bash
git clone https://github.com/YOUR_USERNAME/gcp-audit-cli.git
cd gcp-audit-cli
```
2. Create virtual python env
```bash
python3 -m venv ~/gcp-venv
source ~/gcp-venv/bin/activate  
```
3. Install dependancies
```bash
pip install -r requirements.txt
```
4. Run the cli
```bash
python gcp-audit.py --project YOUR_PROJECT_ID
```

### Example output
```bash
[DEBUG] Fetched 6 service accounts
[DEBUG] Fetched 30 project-level IAM members
[DEBUG] Fetched 0 GKE clusters
[DEBUG] Fetched 5 buckets
[DEBUG] Fetched 1 Cloud Run service
[DEBUG] Fetched 0 Cloud Functions
[DEBUG] Fetched 2 Artifact Registry repositories

## IAM Accounts
Total service accounts: 6
Total IAM members: 30

### Overprivileged Service Accounts
Service account tester@PROJECT.iam.gserviceaccount.com has potentially overprivileged roles

### Users & Custom Service Accounts Roles
tester@PROJECT.iam.gserviceaccount.com -> roles/bigquery.admin
tester2@PROJECT.iam.gserviceaccount.com -> No project-level roles assigned
admin@DOMAIN -> roles/owner

## GKE
No idle clusters detected

## GCS
Bucket gcf-v2-sources-123456789-europe-west2 created 2024-05-21 may be unused

## Cloud Run Services
service-1 -> europe-west1, last update: UNKNOWN, status: Not in use

## Cloud Functions
No Cloud Functions found

## Artifact Registry Repositories
projects/PROJECT/locations/europe-west1/repositories/repo1 -> format: DOCKER, last update: 2025-12-15, status: Active
projects/PROJECT/locations/europe-west1/repositories/repo2 -> format: MAVEN, last update: 2024-12-20, status: Inactive
```
