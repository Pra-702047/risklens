from app.modules.sla.service import calculate_and_assign_sla
from app.modules.sla.models import SLAPolicy, SLAStatus
from datetime import datetime, timezone, timedelta

class MockQuery:
    def __init__(self, items):
        self.items = items
    def filter(self, *args, **kwargs):
        return self
    def first(self):
        return self.items[0] if self.items else None

class MockDB:
    def __init__(self, policy):
        self.policy = policy
        self.added = []
        
    def query(self, model):
        return MockQuery([self.policy] if self.policy else [])
        
    def add(self, item):
        self.added.append(item)
        
    def commit(self):
        pass
        
    def refresh(self, item):
        pass

def test_sla_calculation():
    policy = SLAPolicy(
        id="pol_1",
        priority="P1",
        resolution_time_hours=8,
        warning_time_hours=2,
        escalation_time_hours=10
    )
    
    db = MockDB(policy)
    
    status = calculate_and_assign_sla(db, "comp_1", "P1")
    
    # Check warning is 2 hours BEFORE resolution
    expected_warning = status.due_at - timedelta(hours=2)
    assert status.warning_at == expected_warning
    
    # Check escalate is 10 hours AFTER resolution
    expected_escalate = status.due_at + timedelta(hours=10)
    assert status.escalate_at == expected_escalate
    
    assert status.status == "ON_TRACK"
