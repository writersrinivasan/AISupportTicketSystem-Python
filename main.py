"""
AI Support Ticket System - Main Interface
Minimal CLI interface for testing and demonstration
"""

import json
from ticket_ai import TicketAI


def main():
    """Interactive CLI for the AI support ticket system"""
    ai = TicketAI()
    
    print("🎫 AI Support Ticket System")
    print("Minimal, token-efficient design for engineering teams")
    print("Type 'help' for commands, 'quit' to exit\n")
    
    while True:
        try:
            user_input = input(">>> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if user_input.lower() == 'help':
                show_help()
                continue
            
            if user_input.lower() == 'stats':
                show_stats(ai)
                continue
            
            if not user_input:
                continue
            
            # Process with AI
            response = ai.process(user_input)
            print(json.dumps(response, indent=2))
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def show_help():
    """Display help information"""
    help_text = """
📋 Available Commands:

CREATE:
  • "create ticket for login bug, high priority"
  • "new ticket: API timeout in production"
  
UPDATE:  
  • "update T001 to in progress, investigating"
  • "change T002 status to done"
  
VIEW:
  • "show open tickets"
  • "view T001" 
  • "list high priority tickets"
  
CLOSE:
  • "close T001, fixed configuration"
  • "resolve T002, updated documentation"

SYSTEM:
  • help - show this help
  • stats - show system statistics  
  • quit - exit system

🏷️  Categories: code, infra, doc, other
🔥 Priorities: high (1), med (2), low (3)
📊 Status: open, prog, done
"""
    print(help_text)


def show_stats(ai: TicketAI):
    """Display system statistics"""
    tickets = ai.manager.tickets
    
    if not tickets:
        print("No tickets in system")
        return
    
    # Count by status
    status_counts = {"open": 0, "prog": 0, "done": 0}
    category_counts = {"code": 0, "infra": 0, "doc": 0, "other": 0}
    priority_counts = {1: 0, 2: 0, 3: 0}
    
    for ticket in tickets.values():
        status_counts[ticket["stat"]] += 1
        category_counts[ticket["cat"]] += 1  
        priority_counts[ticket["pri"]] += 1
    
    print(f"""
📊 System Statistics:

Total Tickets: {len(tickets)}

Status:
  • Open: {status_counts['open']}
  • In Progress: {status_counts['prog']} 
  • Done: {status_counts['done']}

Categories:
  • Code: {category_counts['code']}
  • Infrastructure: {category_counts['infra']}
  • Documentation: {category_counts['doc']}
  • Other: {category_counts['other']}

Priorities:
  • High (1): {priority_counts[1]}
  • Medium (2): {priority_counts[2]}
  • Low (3): {priority_counts[3]}
""")


if __name__ == "__main__":
    main()
