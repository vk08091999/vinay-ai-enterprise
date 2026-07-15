import uuid
import time
from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class OrgTenant:
    id: str
    name: str
    custom_domain: str
    billing_status: str = "Active"
    branding: Dict[str, str] = field(default_factory=lambda: {"primary_color": "#8C7BFA", "secondary_color": "#4FD1C5"})

@dataclass
class TeamMember:
    id: str
    org_id: str
    email: str
    role: str
    department: str

class EnterpriseCollaborationPlatform:
    def __init__(self):
        self.tenants = {}
        self.members = {}
        self.rate_limits = {}

    def create_tenant(self, name: str, domain: str) -> OrgTenant:
        tenant_id = f"org_{uuid.uuid4().hex[:8]}"
        tenant = OrgTenant(id=tenant_id, name=name, custom_domain=domain)
        self.tenants[tenant_id] = tenant
        self.members[tenant_id] = []
        return tenant

    def add_member(self, org_id: str, email: str, role: str, department: str) -> TeamMember:
        if org_id not in self.tenants:
            raise KeyError("Invalid Org ID")
        member = TeamMember(id=f"usr_{uuid.uuid4().hex[:8]}", org_id=org_id, email=email, role=role, department=department)
        self.members[org_id].append(member)
        return member

    def verify_isolation_gate(self, actor: TeamMember, target_org_id: str) -> bool:
        if actor.org_id != target_org_id:
            raise PermissionError(f"SECURITY ALERT: Unauthorized access attempt by {actor.id}")
        return True

    def configure_api_key(self, org_id: str, key_alias: str, rps_limit: int = 10):
        self.rate_limits[org_id] = {"alias": key_alias, "max_rps": rps_limit, "current_hits": 0, "window_start": time.time()}

    def check_rate_limit(self, org_id: str) -> bool:
        policy = self.rate_limits.get(org_id)
        if not policy:
            return True
        now = time.time()
        if now - policy["window_start"] > 1.0:
            policy["current_hits"] = 1
            policy["window_start"] = now
            return True
        if policy["current_hits"] >= policy["max_rps"]:
            return False
        policy["current_hits"] += 1
        return True
