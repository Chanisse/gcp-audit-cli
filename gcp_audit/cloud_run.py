from googleapiclient import discovery
from datetime import datetime, timedelta, timezone

# -----------------------------
# Cloud Run Helpers
# -----------------------------

def fetch_cloud_run_services(project, idle_days=30):
    """
    Fetch all Cloud Run services across regions
    Marks services as 'Not in use' if last deployment is older than idle_days
    or unknown
    """
    run = discovery.build('run', 'v1')
    parent = f"projects/{project}/locations/-"
    services = []
    threshold = datetime.now(timezone.utc) - timedelta(days=idle_days)

    try:
        response = run.projects().locations().services().list(parent=parent).execute()
        for s in response.get('items', []):
            name = s['metadata']['name']
            region = s['metadata'].get('namespace', 'UNKNOWN')

            update_time_str = s.get('status', {}).get('latestReadyRevisionTime') or s['metadata'].get('creationTimestamp')
            if update_time_str:
                try:
                    update_time = datetime.strptime(update_time_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                except ValueError:
                    update_time = None
            else:
                update_time = None

            status = "Not in use" if not update_time or update_time < threshold else "Active"

            services.append({
                'name': name,
                'region': region,
                'update_time': update_time,
                'status': status
            })
    except Exception:
        pass

    print(f"[DEBUG] Fetched {len(services)} Cloud Run services")
    return services
