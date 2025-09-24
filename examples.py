"""
AI Support Ticket System - Usage Examples
Demonstrates minimal token usage patterns
"""

import json
from ticket_ai import TicketAI


def main():
    """Run example interactions to demonstrate the system"""
    ai = TicketAI()
    
    print("=== AI Support Ticket System Demo ===")
    print("Token-efficient responses for engineering teams\n")
    
    # Example interactions from the architecture document
    examples = [
        "Create ticket: API timeout issues in production, medium priority",
        "Update T001 to in progress, investigating load balancer", 
        "Show me open high priority tickets",
        "Close T001, fixed load balancer configuration",
        "Create new ticket for login bug, high priority",
        "View T002",
        "Show done tickets"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"Example {i}:")
        print(f"User: {example}")
        
        response = ai.process(example)
        print(f"AI: {json.dumps(response, indent=2)}")
        print("-" * 50)
    
    print("\n=== System Statistics ===")
    
    # Show token efficiency
    sample_response = ai.process("Show open tickets")
    token_count = len(json.dumps(sample_response).split())
    print(f"Avg response tokens: ~{token_count}")
    print(f"Total tickets in system: {len(ai.manager.tickets)}")
    
    print("\n=== Available Commands ===")
    commands = {
        "Create": "create ticket [title] [description] [priority]",
        "Update": "update [ID] [status] [note]",
        "View": "show [status] tickets OR view [ID]", 
        "Close": "close [ID] [resolution]"
    }
    
    for cmd, syntax in commands.items():
        print(f"{cmd}: {syntax}")


if __name__ == "__main__":
    main()
