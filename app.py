"""
AI Support Ticket System - Web Interface
Flask web app to demonstrate the system in localhost browser
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from datetime import datetime
from ticket_ai import TicketAI


app = Flask(__name__)
ai = TicketAI()


@app.route('/')
def index():
    """Main dashboard showing system overview"""
    # Get system statistics
    tickets = ai.manager.tickets
    
    stats = {
        'total': len(tickets),
        'open': len([t for t in tickets.values() if t['stat'] == 'open']),
        'in_progress': len([t for t in tickets.values() if t['stat'] == 'prog']),
        'done': len([t for t in tickets.values() if t['stat'] == 'done']),
        'high_priority': len([t for t in tickets.values() if t['pri'] == 1]),
        'categories': {
            'code': len([t for t in tickets.values() if t['cat'] == 'code']),
            'infra': len([t for t in tickets.values() if t['cat'] == 'infra']),
            'doc': len([t for t in tickets.values() if t['cat'] == 'doc']),
            'other': len([t for t in tickets.values() if t['cat'] == 'other'])
        }
    }
    
    # Get recent tickets (last 5)
    recent_tickets = list(tickets.values())[-5:] if tickets else []
    
    return render_template('dashboard.html', stats=stats, recent_tickets=recent_tickets)


@app.route('/chat')
def chat():
    """Interactive AI chat interface"""
    return render_template('chat.html')


@app.route('/api/process', methods=['POST'])
def api_process():
    """API endpoint to process natural language requests"""
    data = request.get_json()
    user_input = data.get('message', '').strip()
    
    if not user_input:
        return jsonify({'error': 'Empty message'}), 400
    
    try:
        response = ai.process(user_input)
        return jsonify({
            'user_input': user_input,
            'ai_response': response,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/tickets')
def list_tickets():
    """View all tickets"""
    tickets = ai.manager.tickets
    return render_template('tickets.html', tickets=tickets)


@app.route('/api/tickets')
def api_tickets():
    """API to get tickets data"""
    return jsonify(ai.manager.tickets)


@app.route('/demo')
def demo():
    """Demo page with example interactions"""
    examples = [
        "Create ticket for login bug, high priority",
        "Create ticket: API timeout in production, medium priority", 
        "Show open tickets",
        "Update T001 to in progress, investigating issue",
        "Close T001, fixed authentication bug",
        "Show high priority tickets"
    ]
    return render_template('demo.html', examples=examples)


@app.route('/architecture')
def architecture():
    """Show system architecture and token efficiency"""
    try:
        with open('ARCHITECTURE.md', 'r') as f:
            architecture_content = f.read()
    except FileNotFoundError:
        architecture_content = "Architecture document not found"
    
    # Token efficiency demo
    sample_responses = [
        ai.process("Create test ticket"),
        ai.process("Show all tickets")
    ]
    
    token_analysis = []
    for response in sample_responses:
        json_str = json.dumps(response)
        token_count = len(json_str.split()) + json_str.count(',') + json_str.count(':')
        token_analysis.append({
            'response': response,
            'json_str': json_str,
            'estimated_tokens': token_count
        })
    
    return render_template('architecture.html', 
                         architecture=architecture_content,
                         token_analysis=token_analysis)


if __name__ == '__main__':
    # Create some sample tickets for demo
    if not ai.manager.tickets:
        print("Creating sample tickets for demo...")
        try:
            ai.process("Create ticket for database connection timeout, high priority")
            ai.process("Create ticket: Update documentation for new API endpoints")
            ai.process("Create ticket for server deployment automation, medium priority")
            ai.process("Update T001 to in progress, investigating connection pool")
            print(f"Created {len(ai.manager.tickets)} sample tickets")
        except Exception as e:
            print(f"Error creating sample tickets: {e}")
        
    print("🎫 AI Support Ticket System Web Interface")
    print("📊 Token-efficient design for engineering teams")
    print("🚀 Starting server on http://localhost:8080")
    print("📝 Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=False, host='0.0.0.0', port=8080, threaded=True)
    except Exception as e:
        print(f"Error starting server: {e}")
