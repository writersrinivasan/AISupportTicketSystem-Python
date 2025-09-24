# AI-Powered Support Ticket System Architecture
## Minimal, Token-Efficient Design for Engineering & Consulting Companies

---

## Step 1: Core Requirements (Minimal Feature Set)

### Essential Features Only:
1. **Ticket Creation** - Create new support requests
2. **Ticket Classification** - Categorize by type and priority  
3. **Status Tracking** - Monitor ticket progress
4. **Resolution Updates** - Add notes and close tickets
5. **Basic Retrieval** - Search and view tickets

### Excluded "Nice-to-Have" Features:
- File attachments
- Email notifications
- Advanced reporting
- User management system
- Complex workflows
- Time tracking
- SLA management

---

## Step 2: Roles and System Flow

### User Roles:
- **Engineer/Consultant**: Create, update, view tickets
- **Admin**: All operations + system management

### Interaction Flow:
```
User Input → AI Parser → Action Router → Data Handler → Response Generator
```

### Core Actions:
1. `CREATE` - New ticket
2. `UPDATE` - Modify existing ticket
3. `VIEW` - Retrieve ticket(s)
4. `CLOSE` - Resolve ticket

---

## Step 3: Lightweight Data Schema

### Ticket Schema (Token-Optimized):
```json
{
  "id": "T001",           // 4 chars max
  "title": "string",      // 50 chars max
  "desc": "string",       // 200 chars max  
  "cat": "code",          // Enum: code|infra|doc|other
  "pri": 2,               // 1=high, 2=med, 3=low
  "stat": "open",         // Enum: open|prog|done
  "created": "2024-01-15",// YYYY-MM-DD
  "res": "string"         // Resolution note, 100 chars max
}
```

### Categories (4-char codes):
- `code` - Code issues, bugs, development
- `infra` - Infrastructure, deployment, DevOps  
- `doc` - Documentation, requirements
- `other` - General requests

---

## Step 4: AI Interaction Patterns

### Input Pattern:
**Natural Language → Structured Command**

User: "Create ticket for login bug, high priority"
AI Parses: `{action: "CREATE", cat: "code", pri: 1, title: "login bug"}`

### Output Pattern:
**Compressed JSON Response**

```json
{
  "status": "ok",
  "data": {
    "id": "T042",
    "title": "login bug", 
    "cat": "code",
    "pri": 1,
    "stat": "open"
  }
}
```

### Response Codes (2 chars):
- `ok` - Success
- `nf` - Not found  
- `er` - Error
- `up` - Updated

---

## Step 5: Example Dialogues

### Example 1: Create New Ticket
**User:** "Create ticket: API timeout issues in production, medium priority"

**AI Response:**
```json
{
  "status": "ok",
  "action": "created",
  "data": {
    "id": "T043", 
    "title": "API timeout issues in production",
    "cat": "infra",
    "pri": 2,
    "stat": "open",
    "created": "2024-09-24"
  }
}
```

### Example 2: Update Ticket Status  
**User:** "Update T043 to in progress, investigating load balancer"

**AI Response:**
```json
{
  "status": "ok", 
  "action": "updated",
  "data": {
    "id": "T043",
    "stat": "prog",
    "res": "investigating load balancer"
  }
}
```

### Example 3: Retrieve Ticket Summary
**User:** "Show me open high priority tickets"

**AI Response:**
```json
{
  "status": "ok",
  "count": 2, 
  "data": [
    {"id": "T040", "title": "DB connection fails", "cat": "infra", "pri": 1},
    {"id": "T041", "title": "Build pipeline broken", "cat": "code", "pri": 1}
  ]
}
```

### Example 4: Close/Resolve Ticket
**User:** "Close T043, fixed load balancer configuration"

**AI Response:**
```json
{
  "status": "ok",
  "action": "closed", 
  "data": {
    "id": "T043",
    "stat": "done",
    "res": "fixed load balancer configuration"
  }
}
```

---

## Step 6: Token Usage Optimizations

### 1. Compressed Response Format
- Use abbreviated field names (`desc` vs `description`)
- Enum values instead of full strings (`prog` vs `in_progress`)
- Omit null/default values
- Use arrays for bulk operations

### 2. Standardized Templates
```python
# Template responses (pre-computed)
TEMPLATES = {
    "created": '{"status":"ok","action":"created","data":{}}',
    "updated": '{"status":"ok","action":"updated","data":{}}', 
    "error": '{"status":"er","msg":"{}"}'
}
```

### 3. Batch Operations
```json
{
  "action": "bulk_update",
  "tickets": ["T001", "T002", "T003"],
  "changes": {"stat": "done"}
}
```

### 4. Smart Parsing Rules
- Auto-detect priority from keywords (`urgent`=1, `asap`=1, default=2)
- Auto-categorize from context (`deploy`=infra, `bug`=code)
- Use ticket ID patterns for quick lookup

### 5. Scalability Optimizations
- In-memory caching for frequent lookups
- Indexed JSON storage for persistence
- Pagination for large result sets (max 10 items)
- Delta updates (only changed fields)

---

## Implementation Ready AI System Prompt

### System Prompt Template:
```
You are a support ticket AI for an engineering consulting company. 
Respond ONLY in compressed JSON format using these rules:

FIELDS: id(4char), title(50char), desc(200char), cat(code|infra|doc|other), 
        pri(1|2|3), stat(open|prog|done), created(YYYY-MM-DD), res(100char)

ACTIONS: CREATE, UPDATE, VIEW, CLOSE

RESPONSE: {"status":"ok|nf|er","action":"created|updated|closed","data":{}}

Parse natural language to extract: action, category, priority, title, description.
Auto-assign: ID (T###), created date, default priority=2, default status=open.
Keep responses under 150 tokens maximum.
```

### Usage Pattern:
1. User inputs natural language request
2. AI parses and identifies action type
3. AI validates required fields
4. AI generates compressed JSON response
5. System processes and stores data

---

## Technical Architecture

### File Structure:
```
ai_support_system/
├── ticket_ai.py          # Main AI processing logic
├── ticket_manager.py     # Data management
├── schemas.py           # Data validation
├── templates.py         # Response templates  
├── examples.py          # Usage examples
├── data/
│   └── tickets.json     # Simple JSON storage
└── tests/
    └── test_system.py   # Unit tests
```

This architecture provides a **complete, minimal, and token-efficient** support ticket system ready for implementation. The design prioritizes low token usage while maintaining full functionality for engineering and consulting workflows.
