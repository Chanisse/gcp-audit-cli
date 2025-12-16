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

def check_overprivileged(accounts, account_roles):
    """
    Detect service accounts that may be overprivileged based on their assigned roles.
    Flags accounts that have roles like owner, admin, or editor.
    
    Args:
        accounts: list of service accounts [{'email':..., 'disabled':...}]
        account_roles: dict mapping account_email -> [roles]
    """
    alerts = []
    risky_roles = ["roles/owner", "roles/editor", "roles/viewer", "roles/iam.admin"]
    for sa in accounts:
        email = sa['email']
        roles = account_roles.get(email, [])
        if any(r in roles for r in risky_roles):
            alerts.append(f"Service account {email} has potentially overprivileged roles")
    return alerts


def split_project_members(members):
    """
    Split project members into human users and service accounts
    """
    users = []
    service_accounts = []
    for m in members:
        try:
            member_type, identifier = m['member'].split(':', 1)
        except ValueError:
            continue
        if member_type == 'user':
            users.append({'member': identifier, 'role': m['role']})
        elif member_type == 'serviceAccount':
            service_accounts.append({'member': identifier, 'role': m['role']})
    return users, service_accounts


def map_roles_to_accounts(accounts, members):
    """
    Map all custom service accounts and users to their assigned project-level roles.
    Returns dictionary: { account_email_or_user : [roles] }
    """
    system_prefixes = [
        "service-",
        "compute@",
        "cloudbuild@"
    ]

    custom_sa_emails = [
        sa['email'] for sa in accounts
        if not any(sa['email'].startswith(p) for p in system_prefixes)
    ]

    account_roles = {email: [] for email in custom_sa_emails}

    for m in members:
        try:
            member_type, identifier = m['member'].split(':', 1)
        except ValueError:
            continue
        if member_type == "serviceAccount" and identifier in custom_sa_emails:
            account_roles[identifier].append(m['role'])

    for m in members:
        try:
            member_type, identifier = m['member'].split(':', 1)
        except ValueError:
            continue
        if member_type == 'user':
            if identifier not in account_roles:
                account_roles[identifier] = []
            account_roles[identifier].append(m['role'])

    return account_roles
