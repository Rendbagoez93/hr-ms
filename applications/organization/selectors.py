from django.shortcuts import get_object_or_404

from .models import Department, JobTitle


# ---------------------------------------------------------------------------
# Department selectors
# ---------------------------------------------------------------------------


def get_department_list() -> "DepartmentQuerySet":
    return Department.objects.with_children().order_by("name")


def get_root_departments() -> "DepartmentQuerySet":
    return Department.objects.root().with_children()


def get_department(pk) -> Department:
    return get_object_or_404(Department, pk=pk)


# ---------------------------------------------------------------------------
# JobTitle selectors
# ---------------------------------------------------------------------------


def get_jobtitle_list() -> "JobTitleQuerySet":
    return JobTitle.objects.with_department().order_by("name")


def get_jobtitles_for_department(department_id) -> "JobTitleQuerySet":
    return JobTitle.objects.for_department(department_id).with_department()


def get_jobtitle(pk) -> JobTitle:
    return get_object_or_404(JobTitle, pk=pk)
