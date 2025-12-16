from googleapiclient import discovery
from datetime import datetime, timedelta, timezone

def fetch_cloud_functions(project, idle_days=30):
    cf = discovery.build('cloudfunctions', 'v1')
    parent = f"projects/{project}/locations/-"
    threshold = datetime.now(timezone.utc) - timedelta(days=idle_days)
    functions = []

    try:
        response = cf.projects().locations().functions().list(parent=parent).execute()
        for f in response.get('functions', []):
            name = f['name'].split('/')[-1]
            region = f['name'].split('/')[3] if len(f['name'].split('/')) > 3 else 'UNKNOWN'
            update_time_str = f.get('updateTime') or f.get('createTime')
            
            if update_time_str:
                try:
                    update_time = datetime.strptime(update_time_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                except ValueError:
                    update_time = None
            else:
                update_time = None

            status = "Not in use" if not update_time or update_time < threshold else "Active"

            functions.append({
                'name': name,
                'region': region,
                'update_time': update_time,
                'status': status
            })
    except Exception:
        pass

    print(f"[DEBUG] Fetched {len(functions)} Cloud Functions")
    return functions
