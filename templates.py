"""
AI Support Ticket System - Response Templates
Pre-computed templates to minimize token usage
"""

from typing import Dict


class ResponseTemplates:
    """Pre-computed response templates for minimal token usage"""
    
    # Base templates (no data placeholders)
    BASE = {
        "success": '{"status":"ok"}',
        "not_found": '{"status":"nf","msg":"ticket not found"}',
        "error": '{"status":"er","msg":"{}"}',
        "invalid": '{"status":"er","msg":"invalid input"}'
    }
    
    # Action-specific templates
    ACTIONS = {
        "created": {
            "status": "ok",
            "action": "created",
            "data": {}
        },
        "updated": {
            "status": "ok", 
            "action": "updated",
            "data": {}
        },
        "closed": {
            "status": "ok",
            "action": "closed", 
            "data": {}
        },
        "retrieved": {
            "status": "ok",
            "count": 0,
            "data": []
        }
    }
    
    # Error messages (ultra-short)
    ERRORS = {
        "missing_title": "title required",
        "invalid_id": "invalid ticket id", 
        "invalid_priority": "priority must be 1-3",
        "invalid_category": "invalid category",
        "invalid_status": "invalid status",
        "ticket_exists": "ticket id exists",
        "storage_error": "storage failed"
    }
    
    @staticmethod
    def success_response(action: str, data: Dict) -> Dict:
        """Generate success response with minimal tokens"""
        template = ResponseTemplates.ACTIONS.get(action, ResponseTemplates.ACTIONS["created"])
        template["data"] = data
        return template.copy()
    
    @staticmethod 
    def error_response(error_key: str) -> Dict:
        """Generate error response"""
        return {
            "status": "er",
            "msg": ResponseTemplates.ERRORS.get(error_key, "unknown error")
        }
    
    @staticmethod
    def list_response(tickets: list, count: int = None) -> Dict:
        """Generate list response for ticket queries"""
        return {
            "status": "ok",
            "count": count or len(tickets),
            "data": tickets
        }


# Pre-computed help responses
HELP_RESPONSES = {
    "commands": {
        "status": "ok",
        "data": {
            "create": "create ticket [title] [description] [priority: low|med|high]",
            "update": "update [ticket_id] [status: open|prog|done] [note]", 
            "view": "view [ticket_id] or show [status] tickets",
            "close": "close [ticket_id] [resolution]"
        }
    },
    
    "categories": {
        "status": "ok", 
        "data": {
            "code": "bugs, development issues",
            "infra": "servers, deployment, DevOps", 
            "doc": "documentation, requirements",
            "other": "general requests"
        }
    }
}


# Status code mappings for ultra-short responses
STATUS_CODES = {
    "success": "ok",
    "created": "ok", 
    "updated": "up",
    "deleted": "ok",
    "not_found": "nf", 
    "error": "er",
    "invalid": "er"
}
