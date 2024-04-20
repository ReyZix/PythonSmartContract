import hashlib
import time
from datetime import datetime, timedelta
import json
import os

class VirtualContract:
    def __init__(self, contract_id, contract_terms, involved_parties):
        self.contract_id = contract_id
        self.contract_terms = contract_terms
        self.involved_parties = involved_parties
        self.signatures = {}
        self.contract_executed = False
        self.events = []
        self.create_hash()
        self.reminders = {}
        self.contract_file_path = f"contract_{self.contract_id}.json"
        self.load_contract()

    def create_hash(self):
        # Create a unique hash for the contract using its terms and ID
        contract_string = f"{self.contract_id}-{self.contract_terms}"
        self.contract_hash = hashlib.sha256(contract_string.encode()).hexdigest()
        self.log_event("Contract Created", self.contract_hash)

    def sign(self, party, signature):
        if party in self.involved_parties and party not in self.signatures:
            self.signatures[party] = signature
            self.log_event(f"{party} Signed", signature)
            self.save_contract()
        else:
            print(f"{party} is not authorized to sign this contract or has already signed.")

    def verify_signatures(self):
        # Simulate the verification of signatures
        if len(self.signatures) == len(self.involved_parties):
            self.log_event("All Parties Signed", "Verified")
            return True
        else:
            return False

    def execute_contract(self):
        if self.verify_signatures() and not self.contract_executed:
            self.contract_executed = True
            self.log_event("Contract Executed", "Terms Enforced")
            self.save_contract()
            # Execute the terms of the contract
        else:
            print("Contract cannot be executed until all parties sign.")

    def log_event(self, event, data):
        # Log an event with a timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        self.events.append({'event': event, 'data': data, 'timestamp': timestamp})
        print(f"Event Logged: {event} at {timestamp}")

    def get_contract_events(self):
        # Return a list of all logged events
        return self.events

    def set_reminder(self, party, days_before):
        # Set a reminder for a party to sign the contract
        reminder_date = datetime.now() + timedelta(days=days_before)
        self.reminders[party] = reminder_date.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Reminder set for {party} to sign the contract by {self.reminders[party]}")

    def check_reminders(self):
        # Check if there are any pending reminders
        current_time = datetime.now()
        for party, reminder_time in self.reminders.items():
            if datetime.strptime(reminder_time, "%Y-%m-%d %H:%M:%S") < current_time:
                print(f"Reminder: {party} needs to sign the contract.")

    def save_contract(self):
        # Save the contract state to a file to simulate immutability
        contract_data = {
            'contract_id': self.contract_id,
            'contract_terms': self.contract_terms,
            'involved_parties': self.involved_parties,
            'signatures': self.signatures,
            'contract_executed': self.contract_executed,
            'events': self.events,
            'contract_hash': self.contract_hash
        }
        with open(self.contract_file_path, 'w') as contract_file:
            json.dump(contract_data, contract_file)

    def load_contract(self):
        # Load the contract state from a file if it exists
        if os.path.exists(self.contract_file_path):
            with open(self.contract_file_path, 'r') as contract_file:
                contract_data = json.load(contract_file)
                self.contract_id = contract_data['contract_id']
                self.contract_terms = contract_data['contract_terms']
                self.involved_parties = contract_data['involved_parties']
                self.signatures = contract_data['signatures']
                self.contract_executed = contract_data['contract_executed']
                self.events = contract_data['events']
                self.contract_hash = contract_data['contract_hash']

# Example usage:
contract_terms = "Party A agrees to deliver goods to Party B upon payment."
involved_parties = ['Party A', 'Party B']

virtual_contract = VirtualContract('001', contract_terms, involved_parties)

# Set reminders for parties to sign the contract
virtual_contract.set_reminder('Party A', 3)  # Reminder in 3 days
virtual_contract.set_reminder('Party B', 5)  # Reminder in 5 days

# Parties sign the contract
virtual_contract.sign('Party A', 'SignatureA')
virtual_contract.sign('Party B', 'SignatureB')

# Check reminders
virtual_contract.check_reminders()

# Execute the contract
virtual_contract.execute_contract()

# Retrieve the contract events
events = virtual_contract.get_contract_events()
for event in events:
    print(event)
