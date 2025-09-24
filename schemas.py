"""
AI Support Ticket System - Core Data Schemas
Token-efficient data structures for minimal usage
"""

from dataclasses import dataclass
from typing import Optional, Literal, Dict, List
from datetime import datetime


# Type aliases for clarity
TicketId = str  # Format: T001-T999
Category = Literal["code", "infra", "doc", "other"] 
Priority = Literal[1, 2, 3]  # 1=high, 2=med, 3=low
Status = Literal["open", "prog", "done"]


@dataclass
class Ticket:
    """Minimal ticket schema - optimized for token efficiency"""
    id: TicketId
    title: str  # max 50 chars
    desc: str   # max 200 chars
    cat: Category
    pri: Priority 
    stat: Status
    created: str  # YYYY-MM-DD format
    res: Optional[str] = None  # max 100 chars
    
    def to_dict(self) -> Dict:
        """Convert to compressed dict format"""
        data = {
            "id": self.id,
            "title": self.title[:50],
            "desc": self.desc[:200], 
            "cat": self.cat,
            "pri": self.pri,
            "stat": self.stat,
            "created": self.created
        }
        if self.res:
            data["res"] = self.res[:100]
        return data
    
    def to_summary(self) -> Dict:
        """Ultra-compact format for listings"""
        return {
            "id": self.id,
            "title": self.title[:30],
            "cat": self.cat,
            "pri": self.pri
        }


@dataclass 
class TicketQuery:
    """Query parameters for ticket retrieval"""
    status: Optional[Status] = None
    category: Optional[Category] = None  
    priority: Optional[Priority] = None
    limit: int = 10  # max results


@dataclass
class ApiResponse:
    """Standardized API response format"""
    status: Literal["ok", "nf", "er", "up"]  # ok/notfound/error/updated
    action: Optional[str] = None
    data: Optional[Dict | List] = None
    msg: Optional[str] = None  # error messages only
    
    def to_json(self) -> Dict:
        """Convert to minimal JSON format"""
        result = {"status": self.status}
        if self.action:
            result["action"] = self.action
        if self.data is not None:
            result["data"] = self.data
        if self.msg:
            result["msg"] = self.msg
        return result


# Category keywords for auto-classification
CATEGORY_KEYWORDS = {
    "code": ["bug", "error", "exception", "build", "compile", "deploy", "ci/cd"],
    "infra": ["server", "network", "database", "performance", "outage", "aws", "azure"],
    "doc": ["documentation", "readme", "guide", "manual", "wiki", "spec"],
    "other": ["meeting", "training", "access", "account", "general"]
}

# Priority keywords for auto-classification  
PRIORITY_KEYWORDS = {
    1: ["urgent", "critical", "asap", "emergency", "outage", "down", "high"],
    2: ["medium", "normal", "standard", "med"],
    3: ["low", "minor", "enhancement", "nice-to-have"]
}
