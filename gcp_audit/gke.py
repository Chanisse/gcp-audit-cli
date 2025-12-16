from google.cloud import container_v1
from datetime import datetime, timedelta, timezone

# -----------------------------
# GKE Helpers
# -----------------------------

from google.cloud import container_v1
from datetime import datetime, timedelta, timezone

def fetch_gke_clusters(project, idle_days=30):
    client = container_v1.ClusterManagerClient()
    parent = f"projects/{project}/locations/-"
    clusters = client.list_clusters(parent=parent)
    clusters_list = clusters.clusters if clusters.clusters else []

    threshold = datetime.now(timezone.utc) - timedelta(days=idle_days)
    structured_clusters = []

    for c in clusters_list:
        create_time = c.create_time.ToDatetime() if hasattr(c, 'create_time') else None
        status = "Not in use" if not create_time or create_time < threshold else "Active"

        structured_clusters.append({
            'name': c.name,
            'region': c.location,
            'create_time': create_time,
            'status': status
        })

    print(f"[DEBUG] Fetched {len(structured_clusters)} GKE clusters")
    return structured_clusters


def check_idle_clusters(clusters, idle_days=30):
    alerts = []
    threshold = datetime.now(timezone.utc) - timedelta(days=idle_days)
    for c in clusters:
        create_time = c.create_time.ToDatetime() if hasattr(c, 'create_time') else datetime.now(timezone.utc)
        if create_time < threshold:
            alerts.append(f"GKE cluster {c.name} created {create_time.date()} may be idle")
    return alerts
