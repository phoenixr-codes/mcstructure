from mcstructure import Block

def test_stringify():
    b = Block("minecraft:wool", color="red")
    assert b.stringify() == 'minecraft:wool ["color": "red"]'
    assert b.stringify(with_namespace=False) == 'wool ["color": "red"]'
    assert b.stringify(with_states=False) == 'minecraft:wool'
    assert b.stringify(with_namespace=False, with_states=False) == 'wool'

