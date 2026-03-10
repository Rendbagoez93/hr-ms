from enum import StrEnum


class ImportType(StrEnum):
    EMPLOYEE = "employee"
    EMERGENCY_CONTACT = "emergency_contact"
    EMPLOYMENT = "employment"
    CONTRACT = "contract"
    SALARY = "salary"
    DEPARTMENT = "department"
    JOB_TITLE = "job_title"

    @classmethod
    def choices(cls):
        return [(t.value, t.name.replace("_", " ").title()) for t in cls]

    @classmethod
    def label(cls, value: str) -> str:
        return value.replace("_", " ").title()


class ImportStatus(StrEnum):
    PENDING = "pending"
    MAPPING = "mapping"
    READY = "ready"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"

    @classmethod
    def choices(cls):
        return [(s.value, s.name.replace("_", " ").title()) for s in cls]


class FileType(StrEnum):
    CSV = "csv"
    XLSX = "xlsx"

    @classmethod
    def choices(cls):
        return [(f.value, f.value.upper()) for f in cls]


class ImportLogStatus(StrEnum):
    SUCCESS = "success"
    ERROR = "error"
    SKIPPED = "skipped"

    @classmethod
    def choices(cls):
        return [(s.value, s.name.title()) for s in cls]


# Maps each import type to its canonical model field names, verbose labels, and required flag.
# Structure: { import_type: { field_name: (verbose_label, is_required) } }
IMPORT_FIELD_DEFINITIONS: dict[str, dict[str, tuple[str, bool]]] = {
    ImportType.EMPLOYEE: {
        "employee_id": ("Employee ID", True),
        "first_name": ("First Name", True),
        "last_name": ("Last Name", True),
        "date_of_birth": ("Date of Birth", True),
        "gender": ("Gender", True),
        "nationality": ("Nationality", False),
        "national_id": ("National ID", False),
        "phone": ("Phone", False),
        "personal_email": ("Personal Email", False),
        "address_line_1": ("Address Line 1", False),
        "address_line_2": ("Address Line 2", False),
        "city": ("City", False),
        "state_province": ("State / Province", False),
        "postal_code": ("Postal Code", False),
        "country": ("Country", False),
    },
    ImportType.EMERGENCY_CONTACT: {
        "employee_id": ("Employee ID", True),
        "name": ("Contact Name", True),
        "relationship": ("Relationship", True),
        "phone": ("Phone", True),
        "email": ("Email", False),
        "address": ("Address", False),
        "is_primary": ("Is Primary", False),
    },
    ImportType.EMPLOYMENT: {
        "employee_id": ("Employee ID", True),
        "department_code": ("Department Code", True),
        "job_title_code": ("Job Title Code", True),
        "work_location": ("Work Location", False),
        "status": ("Status", False),
        "hire_date": ("Hire Date", True),
        "end_date": ("End Date", False),
    },
    ImportType.CONTRACT: {
        "employee_id": ("Employee ID", True),
        "contract_type": ("Contract Type", True),
        "start_date": ("Start Date", True),
        "end_date": ("End Date", False),
        "terms": ("Terms", False),
    },
    ImportType.SALARY: {
        "employee_id": ("Employee ID", True),
        "pay_grade": ("Pay Grade", False),
        "amount": ("Amount", True),
        "currency": ("Currency", False),
        "payment_frequency": ("Payment Frequency", True),
        "effective_date": ("Effective Date", True),
        "end_date": ("End Date", False),
        "notes": ("Notes", False),
    },
    ImportType.DEPARTMENT: {
        "name": ("Department Name", True),
        "code": ("Code", True),
        "description": ("Description", False),
        "parent_code": ("Parent Department Code", False),
    },
    ImportType.JOB_TITLE: {
        "name": ("Job Title Name", True),
        "code": ("Code", True),
        "description": ("Description", False),
        "department_code": ("Department Code", False),
    },
}

# Aliases used for auto-detection: field_name → list of lowercase header variations
FIELD_ALIASES: dict[str, list[str]] = {
    "employee_id": ["employee_id", "employee id", "emp_id", "emp id", "employee number", "emp no", "staff id", "nik"],
    "first_name": ["first_name", "first name", "firstname", "given name", "nama depan", "nama pertama"],
    "last_name": ["last_name", "last name", "lastname", "surname", "family name", "nama belakang"],
    "date_of_birth": ["date_of_birth", "date of birth", "dob", "birth date", "birthdate", "tanggal lahir"],
    "gender": ["gender", "sex", "jenis kelamin"],
    "nationality": ["nationality", "kewarganegaraan"],
    "national_id": ["national_id", "national id", "ktp", "nik", "id number"],
    "phone": ["phone", "phone number", "telephone", "tel", "mobile", "hp", "no hp", "nomor hp"],
    "personal_email": ["personal_email", "personal email", "email", "e-mail", "email address"],
    "address_line_1": ["address_line_1", "address line 1", "address", "street", "alamat"],
    "address_line_2": ["address_line_2", "address line 2", "alamat 2"],
    "city": ["city", "kota"],
    "state_province": ["state_province", "state", "province", "provinsi"],
    "postal_code": ["postal_code", "postal code", "zip", "zip code", "kode pos"],
    "country": ["country", "negara"],
    "name": ["name", "nama"],
    "relationship": ["relationship", "hubungan"],
    "is_primary": ["is_primary", "is primary", "primary", "utama"],
    "department_code": ["department_code", "department code", "dept code", "dept_code", "kode departemen"],
    "job_title_code": ["job_title_code", "job title code", "title code", "position code", "kode jabatan"],
    "work_location": ["work_location", "work location", "lokasi kerja", "location type"],
    "status": ["status", "employment status"],
    "hire_date": ["hire_date", "hire date", "start date", "join date", "tanggal masuk", "tgl masuk"],
    "end_date": ["end_date", "end date", "termination date", "tanggal selesai"],
    "contract_type": ["contract_type", "contract type", "tipe kontrak"],
    "start_date": ["start_date", "start date"],
    "pay_grade": ["pay_grade", "pay grade", "grade"],
    "amount": ["amount", "salary", "gaji", "nominal", "basic salary", "gaji pokok"],
    "currency": ["currency", "mata uang"],
    "payment_frequency": ["payment_frequency", "payment frequency", "pay frequency", "frekuensi bayar"],
    "effective_date": ["effective_date", "effective date", "berlaku mulai"],
    "notes": ["notes", "note", "catatan", "keterangan"],
    "terms": ["terms", "contract terms", "syarat"],
    "description": ["description", "desc", "keterangan", "deskripsi"],
    "parent_code": ["parent_code", "parent code", "parent department", "kode induk"],
    "code": ["code", "kode"],
}
