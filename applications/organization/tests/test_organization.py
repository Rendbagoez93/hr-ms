import pytest

from applications.factories import DepartmentFactory, EmployeeFactory, EmploymentFactory, JobTitleFactory
from applications.organization.models import Department, JobTitle


pytestmark = pytest.mark.django_db


# ─── Department model ─────────────────────────────────────────────────────────


class TestDepartmentModel:
    def test_str_representation(self, db):
        dept = DepartmentFactory(name="Engineering")
        assert str(dept) == "Engineering"

    def test_unique_name_constraint(self, db):
        DepartmentFactory(name="Finance")
        with pytest.raises(Exception):
            DepartmentFactory(name="Finance")

    def test_unique_code_constraint(self, db):
        DepartmentFactory(code="FIN001")
        with pytest.raises(Exception):
            DepartmentFactory(code="FIN001")

    def test_root_department_has_no_parent(self, db):
        dept = DepartmentFactory(parent=None)
        assert dept.parent is None

    def test_child_department_linked_to_parent(self, db):
        parent = DepartmentFactory(name="Technology")
        child = DepartmentFactory(name="Backend", parent=parent)
        assert child.parent == parent

    def test_parent_set_null_on_parent_delete(self, db):
        parent = DepartmentFactory(name="Corporate")
        child = DepartmentFactory(name="Procurement", parent=parent)
        parent.hard_delete()
        child.refresh_from_db()
        assert child.parent is None

    def test_description_is_optional(self, db):
        dept = DepartmentFactory(description="")
        assert dept.pk is not None

    def test_soft_delete_excludes_from_default_queryset(self, db):
        dept = DepartmentFactory()
        pk = dept.pk
        dept.delete()
        assert not Department.objects.filter(pk=pk).exists()

    def test_restore_brings_back_department(self, db):
        dept = DepartmentFactory()
        pk = dept.pk
        dept.delete()
        dept.restore()
        assert Department.objects.filter(pk=pk).exists()

    def test_ordering_is_alphabetical(self, db):
        DepartmentFactory(name="Zebra Dept")
        DepartmentFactory(name="Alpha Dept")
        names = list(Department.objects.values_list("name", flat=True))
        assert names == sorted(names)


# ─── DepartmentManager / QuerySet ────────────────────────────────────────────


class TestDepartmentManager:
    def test_active_returns_active_departments(self, db):
        active = DepartmentFactory(is_active=True)
        inactive = DepartmentFactory(is_active=False)
        pks = Department.objects.active().values_list("pk", flat=True)
        assert active.pk in pks
        assert inactive.pk not in pks

    def test_root_returns_departments_without_parent(self, db):
        root = DepartmentFactory(parent=None)
        child = DepartmentFactory(parent=root)
        root_pks = Department.objects.root().values_list("pk", flat=True)
        assert root.pk in root_pks
        assert child.pk not in root_pks

    def test_with_children_prefetches_children(self, db):
        parent = DepartmentFactory()
        DepartmentFactory(parent=parent)
        DepartmentFactory(parent=parent)

        result = Department.objects.with_children().get(pk=parent.pk)
        # children already prefetched
        assert len(result.children.all()) == 2

    def test_default_manager_excludes_soft_deleted(self, db):
        dept = DepartmentFactory()
        dept.delete()
        assert dept.pk not in Department.objects.values_list("pk", flat=True)

    def test_root_departments_form_company_tree_top(self, db):
        """HR uses top-level departments to represent the main business units."""
        engineering = DepartmentFactory(name="Engineering Root", parent=None)
        DepartmentFactory(name="Backend Team", parent=engineering)
        DepartmentFactory(name="Frontend Team", parent=engineering)

        root_names = list(Department.objects.root().values_list("name", flat=True))
        assert "Engineering Root" in root_names
        assert "Backend Team" not in root_names


# ─── JobTitle model ───────────────────────────────────────────────────────────


class TestJobTitleModel:
    def test_str_with_department(self, db):
        dept = DepartmentFactory(name="Engineering")
        title = JobTitleFactory(name="Software Engineer", department=dept)
        assert str(title) == "Software Engineer (Engineering)"

    def test_str_without_department(self, db):
        title = JobTitleFactory(name="Contractor", department=None)
        assert str(title) == "Contractor"

    def test_unique_code_constraint(self, db):
        JobTitleFactory(code="SWE001")
        with pytest.raises(Exception):
            JobTitleFactory(code="SWE001")

    def test_unique_name_per_department_constraint(self, db):
        dept = DepartmentFactory()
        JobTitleFactory(name="Manager", department=dept)
        with pytest.raises(Exception):
            JobTitleFactory(name="Manager", department=dept)

    def test_same_name_allowed_in_different_departments(self, db):
        dept1 = DepartmentFactory(name="Sales")
        dept2 = DepartmentFactory(name="Marketing")
        title1 = JobTitleFactory(name="Manager", department=dept1)
        title2 = JobTitleFactory(name="Manager", department=dept2)
        assert title1.pk != title2.pk

    def test_department_foreign_key_nullable(self, db):
        title = JobTitleFactory(department=None)
        assert title.department is None

    def test_soft_delete_excludes_job_title(self, db):
        title = JobTitleFactory()
        pk = title.pk
        title.delete()
        assert not JobTitle.objects.filter(pk=pk).exists()

    def test_ordering_alphabetical(self, db):
        JobTitleFactory(name="Zebra Engineer")
        JobTitleFactory(name="Alpha Engineer")
        names = list(JobTitle.objects.values_list("name", flat=True))
        assert names == sorted(names)

    def test_protected_delete_when_employment_exists(self, db):
        """Deleting a department should be blocked if employments exist."""
        from django.db.models import ProtectedError

        dept = DepartmentFactory()
        EmploymentFactory(department=dept)
        with pytest.raises(ProtectedError):
            dept.hard_delete()


# ─── JobTitleManager / QuerySet ──────────────────────────────────────────────


class TestJobTitleManager:
    def test_active_returns_active_titles(self, db):
        active = JobTitleFactory(is_active=True)
        inactive = JobTitleFactory(is_active=False)
        pks = JobTitle.objects.active().values_list("pk", flat=True)
        assert active.pk in pks
        assert inactive.pk not in pks

    def test_for_department_filters_by_department(self, db):
        dept_a = DepartmentFactory(name="Engineering FA")
        dept_b = DepartmentFactory(name="HR FA")
        title_a = JobTitleFactory(department=dept_a)
        title_b = JobTitleFactory(department=dept_b)

        results = JobTitle.objects.for_department(dept_a.pk)
        assert title_a.pk in results.values_list("pk", flat=True)
        assert title_b.pk not in results.values_list("pk", flat=True)

    def test_with_department_select_related(self, db):
        dept = DepartmentFactory(name="Finance SR")
        JobTitleFactory(department=dept)

        title = JobTitle.objects.with_department().get(department=dept)
        # department already loaded — no extra query
        assert title.department.name == "Finance SR"

    def test_default_manager_excludes_soft_deleted(self, db):
        title = JobTitleFactory()
        title.delete()
        assert title.pk not in JobTitle.objects.values_list("pk", flat=True)

    def test_for_department_returns_empty_for_no_titles(self, db):
        dept = DepartmentFactory(name="Empty Dept")
        assert JobTitle.objects.for_department(dept.pk).count() == 0
