from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    candidate = "candidate"

class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class EmploymentType(str, Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    internship = "internship"

class WorkMode(str, Enum):
    onsite = "onsite"
    remote = "remote"
    hybrid = "hybrid"
