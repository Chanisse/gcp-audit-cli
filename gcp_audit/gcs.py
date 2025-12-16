from google.cloud import storage
from datetime import datetime, timedelta, timezone

# -----------------------------
# GCS Helpers
# -----------------------------

def fetch_buckets(project):
    client = storage.Client(project=project)
    buckets = list(client.list_buckets())
    print(f"[DEBUG] Fetched {len(buckets)} buckets")
    return buckets

def check_idle_buckets(buckets, idle_days=60):
    alerts = []
    threshold = datetime.now(timezone.utc) - timedelta(days=idle_days)
    for b in buckets:
        if b.time_created < threshold:
            alerts.append(f"Bucket {b.name} created {b.time_created.date()} may be unused")
    return alerts
