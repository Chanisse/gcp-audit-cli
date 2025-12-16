from googleapiclient import discovery
from datetime import datetime, timedelta, timezone

# -----------------------------
# Artifact Registry Helpers
# -----------------------------

def fetch_artifact_registry(project, idle_days=90):
    """
    Fetch all Artifact Registry repositories across GCP regions
    Reports last update and flags inactive repos
    """
    ar = discovery.build('artifactregistry', 'v1')
    locations = ['europe-west2']
    all_repos = []
    threshold = datetime.now(timezone.utc) - timedelta(days=idle_days)

    for loc in locations:
        parent = f"projects/{project}/locations/{loc}"
        try:
            response = ar.projects().locations().repositories().list(parent=parent).execute()
            repos = response.get('repositories', [])
            for r in repos:
                update_time_str = r.get('updateTime')
                if update_time_str:
                    update_time = datetime.strptime(update_time_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                else:
                    update_time = None
                active = "Active" if update_time and update_time > threshold else "Inactive"
                all_repos.append({
                    'name': r['name'],
                    'format': r.get('format'),
                    'update_time': update_time,
                    'status': active
                })
        except Exception:
            continue

    print(f"[DEBUG] Fetched {len(all_repos)} Artifact Registry repositories")
    return all_repos
