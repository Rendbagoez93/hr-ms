import pytest


pytestmark = pytest.mark.django_db


# ─── Identity ─────────────────────────────────────────────────────────────────


def test_primary_key_is_uuid(Item):
    import uuid

    obj = Item.objects.create(name="Alice")
    assert isinstance(obj.id, uuid.UUID)


def test_str_representation(Item):
    obj = Item.objects.create(name="Bob")
    assert str(obj) == f"Item({obj.id})"


def test_created_at_is_set_on_create(Item):
    obj = Item.objects.create(name="Carol")
    assert obj.created_at is not None


def test_updated_at_changes_on_save(Item):
    obj = Item.objects.create(name="Dave")
    before = obj.updated_at
    obj.name = "Dave Updated"
    obj.save()
    assert obj.updated_at >= before


# ─── Soft Delete ──────────────────────────────────────────────────────────────


def test_soft_delete_sets_deleted_at(Item):
    obj = Item.objects.create(name="Eve")
    obj.delete()
    assert obj.deleted_at is not None


def test_soft_delete_sets_is_active_false(Item):
    obj = Item.objects.create(name="Frank")
    obj.delete()
    assert obj.is_active is False


def test_soft_deleted_record_excluded_from_default_manager(Item):
    obj = Item.objects.create(name="Grace")
    obj.delete()
    assert not Item.objects.filter(id=obj.id).exists()


def test_soft_deleted_record_in_deleted_objects_manager(Item):
    obj = Item.objects.create(name="Heidi")
    obj.delete()
    assert Item.deleted_objects.filter(id=obj.id).exists()


def test_active_record_not_in_deleted_objects_manager(Item):
    obj = Item.objects.create(name="Ivan")
    assert not Item.deleted_objects.filter(id=obj.id).exists()


# ─── all_objects ──────────────────────────────────────────────────────────────


def test_all_objects_returns_active_records(Item):
    obj = Item.objects.create(name="Judy")
    assert Item.all_objects.filter(id=obj.id).exists()


def test_all_objects_returns_soft_deleted_records(Item):
    obj = Item.objects.create(name="Karl")
    obj.delete()
    assert Item.all_objects.filter(id=obj.id).exists()


def test_all_objects_count_includes_deleted(Item):
    Item.objects.create(name="Laura")
    deleted = Item.objects.create(name="Mallory")
    deleted.delete()
    assert Item.all_objects.count() == 2
    assert Item.objects.count() == 1


# ─── Restore ──────────────────────────────────────────────────────────────────


def test_restore_clears_deleted_at(Item):
    obj = Item.objects.create(name="Niaj")
    obj.delete()
    obj.restore()
    assert obj.deleted_at is None


def test_restore_sets_is_active_true(Item):
    obj = Item.objects.create(name="Oscar")
    obj.delete()
    obj.restore()
    assert obj.is_active is True


def test_restore_makes_record_visible_in_default_manager(Item):
    obj = Item.objects.create(name="Peggy")
    obj.delete()
    obj.restore()
    assert Item.objects.filter(id=obj.id).exists()


def test_restore_removes_record_from_deleted_objects_manager(Item):
    obj = Item.objects.create(name="Quinn")
    obj.delete()
    obj.restore()
    assert not Item.deleted_objects.filter(id=obj.id).exists()


# ─── Hard Delete ──────────────────────────────────────────────────────────────


def test_hard_delete_removes_from_db(Item):
    obj = Item.objects.create(name="Rupert")
    obj.hard_delete()
    assert not Item.all_objects.filter(id=obj.id).exists()
