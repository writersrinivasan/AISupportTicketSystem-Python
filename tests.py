"""
AI Support Ticket System - Unit Tests
Validate core functionality and token efficiency
"""

import unittest
import json
import tempfile
from pathlib import Path

from ticket_ai import TicketAI, TicketManager
from schemas import TicketQuery


class TestTicketManager(unittest.TestCase):
    """Test core ticket management functions"""
    
    def setUp(self):
        """Set up test environment with temporary data file"""
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        self.temp_file.close()
        self.manager = TicketManager(self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary files"""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    def test_create_ticket(self):
        """Test ticket creation"""
        response = self.manager.create_ticket("Test bug", "Description", "code", 1)
        
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["action"], "created")
        self.assertEqual(response["data"]["title"], "Test bug")
        self.assertEqual(response["data"]["cat"], "code")
        self.assertEqual(response["data"]["pri"], 1)
        self.assertEqual(response["data"]["stat"], "open")
    
    def test_update_ticket(self):
        """Test ticket updates"""
        # Create a ticket first
        create_response = self.manager.create_ticket("Test ticket")
        ticket_id = create_response["data"]["id"]
        
        # Update it
        response = self.manager.update_ticket(ticket_id, "prog", "Working on it")
        
        self.assertEqual(response["status"], "ok") 
        self.assertEqual(response["action"], "updated")
        self.assertEqual(response["data"]["stat"], "prog")
        self.assertEqual(response["data"]["res"], "Working on it")
    
    def test_close_ticket(self):
        """Test ticket closure"""
        # Create and close ticket
        create_response = self.manager.create_ticket("Test ticket")
        ticket_id = create_response["data"]["id"]
        
        response = self.manager.close_ticket(ticket_id, "Fixed the issue")
        
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["action"], "closed") 
        self.assertEqual(response["data"]["stat"], "done")
        self.assertEqual(response["data"]["res"], "Fixed the issue")
    
    def test_list_tickets(self):
        """Test ticket listing with filters"""
        # Create test tickets
        self.manager.create_ticket("Bug 1", cat="code", pri=1)
        self.manager.create_ticket("Bug 2", cat="infra", pri=2)
        
        # Test filtering
        query = TicketQuery(category="code")
        response = self.manager.list_tickets(query)
        
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["count"], 1)
        self.assertEqual(response["data"][0]["cat"], "code")


class TestTicketAI(unittest.TestCase):
    """Test AI natural language processing"""
    
    def setUp(self):
        """Set up AI instance with temporary storage"""
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        self.temp_file.close()
        self.ai = TicketAI()
        self.ai.manager = TicketManager(self.temp_file.name)
    
    def tearDown(self):
        """Clean up"""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    def test_create_parsing(self):
        """Test natural language ticket creation"""
        response = self.ai.process("Create ticket for login bug, high priority")
        
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["action"], "created")
        self.assertIn("login bug", response["data"]["title"])
        self.assertEqual(response["data"]["pri"], 1)  # high priority
        self.assertEqual(response["data"]["cat"], "code")  # auto-detected
    
    def test_update_parsing(self):
        """Test ticket update parsing"""
        # Create a ticket first
        create_response = self.ai.process("Create test ticket")
        ticket_id = create_response["data"]["id"]
        
        # Update it
        response = self.ai.process(f"Update {ticket_id} to in progress, investigating issue")
        
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["action"], "updated")
        self.assertEqual(response["data"]["stat"], "prog")
    
    def test_view_parsing(self):
        """Test ticket viewing"""
        # Create test tickets
        self.ai.process("Create open ticket")
        self.ai.process("Create another ticket")
        
        # List all tickets
        response = self.ai.process("Show all tickets")
        
        self.assertEqual(response["status"], "ok")
        self.assertGreaterEqual(response["count"], 2)
    
    def test_close_parsing(self):
        """Test ticket closure parsing"""
        # Create and close ticket
        create_response = self.ai.process("Create test ticket")
        ticket_id = create_response["data"]["id"]
        
        response = self.ai.process(f"Close {ticket_id}, fixed the problem")
        
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["action"], "closed")
        self.assertEqual(response["data"]["stat"], "done")
        self.assertIn("fixed the problem", response["data"]["res"])


class TestTokenEfficiency(unittest.TestCase):
    """Test token usage optimization"""
    
    def setUp(self):
        self.ai = TicketAI()
    
    def test_response_size(self):
        """Verify responses stay under token limits"""
        # Create sample response
        response = self.ai.process("Create test ticket")
        json_str = json.dumps(response)
        
        # Count approximate tokens (words + punctuation)
        token_count = len(json_str.split()) + json_str.count(',') + json_str.count(':')
        
        # Should be under 50 tokens for typical response
        self.assertLess(token_count, 50)
    
    def test_field_abbreviation(self):
        """Verify abbreviated field names are used"""
        response = self.ai.process("Create test ticket")
        data = response["data"]
        
        # Check for abbreviated field names
        self.assertIn("cat", data)  # not "category"
        self.assertIn("pri", data)  # not "priority" 
        self.assertIn("stat", data)  # not "status"
        self.assertIn("desc", data)  # not "description"
    
    def test_enum_values(self):
        """Verify short enum values"""
        response = self.ai.process("Update T001 to in progress")
        
        # Status should be abbreviated
        if response["status"] == "ok":
            self.assertEqual(len(response["data"]["stat"]), 4)  # "prog" not "in_progress"


def run_tests():
    """Run all tests and display results"""
    print("🧪 Running AI Support Ticket System Tests")
    print("=" * 50)
    
    # Create test suite
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestTicketManager))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestTicketAI))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestTokenEfficiency))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Summary
    print(f"\n📊 Test Results:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
        
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
