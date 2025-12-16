#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone

from gcp_audit import iam, gcs, gke, cloud_run, cloud_functions, gar

# -----------------------------
# Report Generation
# -----------------------------

def generate_report(project):
    report = [f"# Audit report for project: {project}\n"]

    # Fetch IAM
    accounts = iam.fetch_iam(project)
    members = iam.fetch_project_iam(project)

    report.append("## IAM Accounts")
    report.append(f"Total service accounts: {len(accounts)}")
    report.append(f"Total IAM members: {len(members)}")

    # GKE
    clusters = gke.fetch_gke_clusters(project)
    cluster_alerts = gke.check_idle_clusters(clusters)
    report.append("\n## GKE")
    report += cluster_alerts if cluster_alerts else ["No idle clusters detected"]

    # GCS
    buckets = gcs.fetch_buckets(project)
    bucket_alerts = gcs.check_idle_buckets(buckets)
    report.append("\n## GCS")
    report += bucket_alerts if bucket_alerts else ["No idle buckets detected"]

    # Cloud Run
    run_services = cloud_run.fetch_cloud_run_services(project)
    report.append("\n## Cloud Run Services")
    if run_services:
        for s in run_services:
            last_update = s['update_time'].date() if s['update_time'] else "UNKNOWN"
            report.append(f"{s['name']} -> {s['region']}, last update: {last_update}, status: {s['status']}")
    else:
        report.append("No Cloud Run services found")

    # Cloud Functions
    functions = cloud_functions.fetch_cloud_functions(project)
    report.append("\n## Cloud Functions")
    if functions:
        for f in functions:
            report.append(f"{f['name']} -> {f.get('status', 'UNKNOWN')}")
    else:
        report.append("No Cloud Functions found")

    # Artifact Registry
    repos = gar.fetch_artifact_registry(project)
    report.append("\n## Artifact Registry Repositories")
    if repos:
        for r in repos:
            last_used = r['update_time'].date() if r['update_time'] else "UNKNOWN"
            report.append(f"{r['name']} -> format: {r['format']}, last update: {last_used}, status: {r['status']}")
    else:
        report.append("No Artifact Registry repositories found")

    return "\n".join(report)

# -----------------------------
# CLI Entrypoint
# -----------------------------

def main():
    parser = argparse.ArgumentParser(description="Personal GCP auditor")
    parser.add_argument("--project", required=True, help="GCP project ID")
    args = parser.parse_args()

    report = generate_report(args.project)
    print(report)

if __name__ == "__main__":
    main()
