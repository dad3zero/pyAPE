from contacts_parser.models.flow_models import Parent

def test_parent_minimal_information():
    parent = Parent("Doe", "John", "john@doe.com")
    assert parent.last_name == "Doe"
    assert parent.first_name == "John"
    assert parent.email == "john@doe.com"
    assert parent.relationship == ""
    assert parent.civility == ""

def test_parent_relationship_information():
    parent = Parent("Doe", "John", "john@doe.com", "père")
    assert parent.last_name == "Doe"
    assert parent.first_name == "John"
    assert parent.email == "john@doe.com"
    assert parent.relationship == "père"
    assert parent.civility == ""
