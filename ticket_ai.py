"""
AI Support Ticket System - Core Logic
Minimal, token-efficient ticket management
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from schemas import Ticket, TicketQuery, ApiResponse, CATEGORY_KEYWORDS, PRIORITY_KEYWORDS
from templates import ResponseTemplates


class TicketManager:
    """Core ticket management with JSON storage"""
    
    def __init__(self, data_file: str = "data/tickets.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(exist_ok=True)
        self._load_data()
    
    def _load_data(self):
        """Load tickets from JSON file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    content = f.read().strip()
                    if content:
                        self.tickets = json.loads(content)
                    else:
                        self.tickets = {}
            except (json.JSONDecodeError, FileNotFoundError):
                self.tickets = {}
        else:
            self.tickets = {}
    
    def _save_data(self):
        """Save tickets to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.tickets, f, indent=2)
    
    def _generate_id(self) -> str:
        """Generate next ticket ID (T001-T999)"""
        if not self.tickets:
            return "T001"
        
        max_num = max([int(tid[1:]) for tid in self.tickets.keys()])
        return f"T{max_num + 1:03d}"
    
    def create_ticket(self, title: str, desc: str = "", 
                     cat: str = "other", pri: int = 2) -> Dict:
        """Create new ticket with validation"""
        if not title:
            return ResponseTemplates.error_response("missing_title")
        
        ticket_id = self._generate_id()
        ticket = Ticket(
            id=ticket_id,
            title=title[:50],
            desc=desc[:200],
            cat=cat,
            pri=pri,
            stat="open", 
            created=datetime.now().strftime("%Y-%m-%d")
        )
        
        self.tickets[ticket_id] = ticket.to_dict()
        self._save_data()
        
        return ResponseTemplates.success_response("created", ticket.to_dict())
    
    def update_ticket(self, ticket_id: str, status: str = None, 
                     resolution: str = None) -> Dict:
        """Update existing ticket"""
        if ticket_id not in self.tickets:
            return ResponseTemplates.error_response("invalid_id")
        
        ticket = self.tickets[ticket_id]
        updated_fields = {}
        
        if status:
            ticket["stat"] = status
            updated_fields["stat"] = status
            
        if resolution:
            ticket["res"] = resolution[:100]
            updated_fields["res"] = resolution[:100]
        
        self._save_data()
        
        response_data = {"id": ticket_id, **updated_fields}
        return ResponseTemplates.success_response("updated", response_data)
    
    def get_ticket(self, ticket_id: str) -> Dict:
        """Retrieve single ticket"""
        if ticket_id not in self.tickets:
            return ResponseTemplates.error_response("invalid_id")
        
        return {"status": "ok", "data": self.tickets[ticket_id]}
    
    def list_tickets(self, query: TicketQuery = None) -> Dict:
        """List tickets with optional filtering"""
        results = []
        
        for ticket in self.tickets.values():
            # Apply filters
            if query:
                if query.status and ticket["stat"] != query.status:
                    continue
                if query.category and ticket["cat"] != query.category:
                    continue  
                if query.priority and ticket["pri"] != query.priority:
                    continue
            
            # Use summary format for listings
            results.append({
                "id": ticket["id"],
                "title": ticket["title"][:30],
                "cat": ticket["cat"], 
                "pri": ticket["pri"]
            })
        
        # Apply limit
        if query and query.limit:
            results = results[:query.limit]
        
        return ResponseTemplates.list_response(results, len(results))
    
    def close_ticket(self, ticket_id: str, resolution: str) -> Dict:
        """Close ticket with resolution"""
        if ticket_id not in self.tickets:
            return ResponseTemplates.error_response("invalid_id")
        
        self.tickets[ticket_id]["stat"] = "done"
        self.tickets[ticket_id]["res"] = resolution[:100]
        self._save_data()
        
        response_data = {
            "id": ticket_id,
            "stat": "done", 
            "res": resolution[:100]
        }
        return ResponseTemplates.success_response("closed", response_data)


class TicketAI:
    """AI interface for natural language ticket operations"""
    
    def __init__(self):
        self.manager = TicketManager()
        self.action_patterns = {
            r'create|new|add': 'create',
            r'update|modify|change': 'update', 
            r'show|view|get|list|find': 'view',
            r'close|resolve|finish|done': 'close'
        }
    
    def _extract_priority(self, text: str) -> int:
        """Auto-detect priority from text (1=high, 2=med, 3=low)"""
        text_lower = text.lower()
        
        for priority, keywords in PRIORITY_KEYWORDS.items():
            if any(keyword in text_lower for keyword in keywords):
                return priority
        
        return 2  # default medium
    
    def _extract_category(self, text: str) -> str:
        """Auto-detect category from text"""
        text_lower = text.lower()
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
                
        return "other"  # default
    
    def _parse_action(self, text: str) -> Optional[str]:
        """Extract action from natural language"""
        text_lower = text.lower()
        
        for pattern, action in self.action_patterns.items():
            if re.search(pattern, text_lower):
                return action
        
        return None
    
    def _extract_ticket_id(self, text: str) -> Optional[str]:
        """Extract ticket ID from text (T001 format)"""
        match = re.search(r'T\d{3}', text.upper())
        return match.group(0) if match else None
    
    def process(self, user_input: str) -> Dict:
        """Main AI processing function - converts natural language to actions"""
        if not user_input:
            return ResponseTemplates.error_response("invalid")
        
        action = self._parse_action(user_input)
        
        if action == "create":
            return self._handle_create(user_input)
        elif action == "update":
            return self._handle_update(user_input)
        elif action == "view":
            return self._handle_view(user_input) 
        elif action == "close":
            return self._handle_close(user_input)
        else:
            return ResponseTemplates.error_response("invalid")
    
    def _handle_create(self, text: str) -> Dict:
        """Handle ticket creation"""
        # Extract title (everything after action keywords)
        title_match = re.search(r'(?:create|new|add)\s+(?:ticket\s+)?(.+)', text, re.IGNORECASE)
        if not title_match:
            return ResponseTemplates.error_response("missing_title")
        
        title = title_match.group(1).strip()
        
        # Extract priority and category
        priority = self._extract_priority(text)
        category = self._extract_category(text)
        
        return self.manager.create_ticket(title, "", category, priority)
    
    def _handle_update(self, text: str) -> Dict:
        """Handle ticket updates"""
        ticket_id = self._extract_ticket_id(text)
        if not ticket_id:
            return ResponseTemplates.error_response("invalid_id")
        
        # Extract status
        status = None
        if any(word in text.lower() for word in ["progress", "prog", "working"]):
            status = "prog"
        elif any(word in text.lower() for word in ["done", "completed", "finished"]):
            status = "done"
        elif any(word in text.lower() for word in ["open", "new"]):
            status = "open"
        
        # Extract resolution/note (everything after ticket ID)
        note_match = re.search(rf'{ticket_id}\s+.*?\s+(.+)', text, re.IGNORECASE)
        resolution = note_match.group(1).strip() if note_match else None
        
        return self.manager.update_ticket(ticket_id, status, resolution)
    
    def _handle_view(self, text: str) -> Dict:
        """Handle ticket viewing"""
        ticket_id = self._extract_ticket_id(text)
        
        if ticket_id:
            # Single ticket view
            return self.manager.get_ticket(ticket_id)
        else:
            # List tickets with filters
            query = TicketQuery()
            
            # Check for status filters
            if "open" in text.lower():
                query.status = "open"
            elif "progress" in text.lower() or "prog" in text.lower():
                query.status = "prog"
            elif "done" in text.lower() or "closed" in text.lower():
                query.status = "done"
            
            # Check for priority filters
            if any(word in text.lower() for word in PRIORITY_KEYWORDS[1]):
                query.priority = 1
            elif any(word in text.lower() for word in PRIORITY_KEYWORDS[3]):
                query.priority = 3
            
            return self.manager.list_tickets(query)
    
    def _handle_close(self, text: str) -> Dict:
        """Handle ticket closure"""
        ticket_id = self._extract_ticket_id(text)
        if not ticket_id:
            return ResponseTemplates.error_response("invalid_id")
        
        # Extract resolution (everything after ticket ID and comma)
        resolution_match = re.search(rf'{ticket_id}[,\s]+(.+)', text, re.IGNORECASE)
        resolution = resolution_match.group(1).strip() if resolution_match else "resolved"
        
        return self.manager.close_ticket(ticket_id, resolution)
