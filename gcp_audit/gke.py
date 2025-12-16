from google.cloud import container_v1
from datetime import datetime, timedelta, timezone

# -----------------------------
# GKE Helpers
# -----------------------------

def fetch_gke_clusters(project):
    client = container_v1.ClusterManagerClient()
    parent = f"projects/{project}/locations/-"
    clusters = client.list_clusters(parent=parent)
    clusters_list = clusters.clusters if clusters.clusters else []
    print(f"[DEBUG] Fetched {len(clusters_list)} GKE clusters")
    return clusters_list

def check_idle_clusters(clusters, idle_days=30):
    alerts = []
    threshold = datetime.now(timezone.utc) - timedelta(days=idle_days)
    for c in clusters:
        create_time = c.create_time.ToDatetime() if hasattr(c, 'create_time') else datetime.now(timezone.utc)
        if create_time < threshold:
            alerts.append(f"GKE cluster {c.name} created {create_time.date()} may be idle")
    return alerts
