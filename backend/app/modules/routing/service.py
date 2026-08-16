from sqlalchemy.orm import Session
from app.modules.routing.models import RoutingRule

def get_routing_for_complaint(db: Session, category: str, zone_id: str = None, issue_priority: str = None) -> str:
    """
    Deterministically find the department_id based on category, zone, and priority.
    """
    
    # 1. Try exact match: Category + Zone + Priority
    if zone_id and issue_priority:
        rule = db.query(RoutingRule).filter(
            RoutingRule.category == category,
            RoutingRule.zone_id == zone_id,
            RoutingRule.issue_priority == issue_priority,
            RoutingRule.is_active == True
        ).order_by(RoutingRule.evaluation_priority.desc()).first()
        if rule: return rule.department_id

    # 2. Try match: Category + Zone
    if zone_id:
        rule = db.query(RoutingRule).filter(
            RoutingRule.category == category,
            RoutingRule.zone_id == zone_id,
            RoutingRule.issue_priority.is_(None),
            RoutingRule.is_active == True
        ).order_by(RoutingRule.evaluation_priority.desc()).first()
        if rule: return rule.department_id
            
    # 3. Try match: Category only
    rule = db.query(RoutingRule).filter(
        RoutingRule.category == category,
        RoutingRule.zone_id.is_(None),
        RoutingRule.issue_priority.is_(None),
        RoutingRule.is_active == True
    ).order_by(RoutingRule.evaluation_priority.desc()).first()
    
    if rule: return rule.department_id
        
    # 3. Fallback routing rule
    fallback_rule = db.query(RoutingRule).filter(
        RoutingRule.category == "FALLBACK",
        RoutingRule.is_active == True
    ).first()
    
    if fallback_rule:
        return fallback_rule.department_id
        
    # Hardcoded safety fallback if DB is completely unconfigured
    return "DEPT_GENERAL_ADMIN"
