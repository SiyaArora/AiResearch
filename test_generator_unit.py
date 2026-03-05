from generate_tuition_emails import TuitionEmailGenerator


def _generator():
    return TuitionEmailGenerator(
        {
            'username': 'u',
            'password': 'p',
            'host': 'h',
            'port': '1521',
            'service_name': 'svc',
        }
    )


def test_parse_numeric_handles_commas_and_invalid_values():
    generator = _generator()
    assert generator.parse_numeric('1,234.56') == 1234.56
    assert generator.parse_numeric(None) == 0.0
    assert generator.parse_numeric('not-a-number') == 0.0


def test_generate_html_email_escapes_injected_html():
    generator = _generator()
    html = generator.generate_html_email(
        {
            'employee_name': '<script>alert(1)</script>',
            'student_name': '<b>Student</b>',
            'relation_to_employee': '<img src=x onerror=1>',
            'major': 'Computer Science',
            'degree': 'BS',
            'college': 'Arts & Sciences',
        }
    )

    assert '<script>alert(1)</script>' not in html
    assert '&lt;script&gt;alert(1)&lt;/script&gt;' in html
    assert '&lt;b&gt;Student&lt;/b&gt;' in html


def test_fetch_tuition_data_rejects_invalid_table_name():
    generator = _generator()
    generator.connection = object()  # bypass connection check for this validation test

    records = generator.fetch_tuition_data('contact_tuition; DROP TABLE users;')

    assert records == []
