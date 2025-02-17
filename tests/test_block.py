from mcstructure import Block


def test_stringify():
    b = Block("minecraft:wool", color="red")
    assert b.stringify() == 'minecraft:wool ["color"="red"]'
    assert b.stringify(with_namespace=False) == 'wool ["color"="red"]'
    assert b.stringify(with_states=False) == "minecraft:wool"
    assert b.stringify(with_namespace=False, with_states=False) == "wool"

    b = Block("minecraft:dispenser", triggered_bit=True)
    assert (
        b.stringify(with_namespace=False, with_states=True)
        == 'dispenser ["triggered_bit"=true]'
    )

    b = Block("minecraft:jigsaw", rotation=12)
    assert (
        b.stringify(with_namespace=False, with_states=True) == 'jigsaw ["rotation"=12]'
    )
