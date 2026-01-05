from enum import Enum


class OrgCapability(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
