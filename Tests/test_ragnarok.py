from RagnarokEngine3.RE3 import Vector2, Vector3, Vector4


def test_vector2():
    vector2 = Vector2(10, 2)
    assert (vector2 * 2) == Vector2(20, 4)
    assert (vector2 / 2) == Vector2(5, 1)
    assert (vector2 - Vector2(5, 1)) == Vector2(5, 1)
    assert (vector2 + Vector2(5, 1)) == Vector2(15, 3)


def test_vector3():
    vector3 = Vector3(10, 2, 1)
    assert (vector3 * 2) == Vector3(20, 4, 2)
    assert (vector3 / 2) == Vector3(5, 1, 0.5)
    assert (vector3 + Vector3(5, 1, 0.5)) == Vector3(15, 3, 1.5)
    assert (vector3 - Vector3(5, 1, 0.5)) == Vector3(5, 1, 0.5)


def test_vector4():
    vector4 = Vector4(10, 2, 1, 0)
    assert (vector4 * 2) == Vector4(20, 4, 2, 0)
    assert (vector4 / 2) == Vector4(5, 1, 0.5, 0)
    assert (vector4 + Vector4(5, 1, 0.5, 0)) == Vector4(15, 3, 1.5, 0)
    assert (vector4 - Vector4(5, 1, 0.5, 0)) == Vector4(5, 1, 0.5, 0)