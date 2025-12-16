from googleapiclient import discovery

# -----------------------------
# IAM / Service Account Helpers
# -----------------------------

def fetch_iam(project):
    """
    List all service accounts in the project using ADC
    """
    service = discovery.build('iam', 'v1')
    name = f'projects/{project}'
    accounts = []

    request = service.projects().serviceAccounts().list(name=name)
    while request:
        response = request.execute()
        for account in response.get('accounts', []):
            accounts.append({
                'email': account['email'],
                'disabled': account.get('disabled', False)
            })
        request = service.projects().serviceAccounts().list_next(request, response)

    # FIXED f-string
    print(f"[DEBUG] Fetched {len(accounts)} service accounts")
    return accounts


def fetch_project_iam(project):
    """
    Fetch project-level IAM bindings
    """
    service = discovery.build('cloudresourcemanager', 'v1')
    policy = service.projects().getIamPolicy(resource=project, body={}).execute()

    members = [{'role': b['role'], 'member': m} 
               for b in policy.get('bindings', []) 
               for m in b.get('members', [])]

    print(f"[DEBUG] Fetched {len(members)} project-level IAM members")
    return members
