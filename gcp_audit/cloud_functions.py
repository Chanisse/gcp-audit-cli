from googleapiclient import discovery

# -----------------------------
# Cloud Functions Helpers
# -----------------------------

def fetch_cloud_functions(project):
    functions = discovery.build('cloudfunctions', 'v1')
    parent = f"projects/{project}/locations/-"
    response = functions.projects().locations().functions().list(parent=parent).execute()
    funcs = []
    for f in response.get('functions', []):
        funcs.append({'name': f['name'], 'status': f.get('status')})
    print(f"[DEBUG] Fetched {len(funcs)} Cloud Functions")
    return funcs
