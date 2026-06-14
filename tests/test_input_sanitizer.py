"""Unit tests for the input sanitization module."""

import pytest  # Test framework

from src.utils.input_sanitizer import (  # Module under test
    sanitize_string,
    validate_date,
    validate_location,
    validate_positive_integer,
)


class TestSanitizeString:
    """Test suite for the sanitize_string function."""

    def test_clean_input_passes_through(self) -> None:
        """Verify that clean input is returned unchanged."""
        result = sanitize_string("New York to London")
        assert result == "New York to London"

    def test_strips_whitespace(self) -> None:
        """Verify that leading and trailing whitespace is removed."""
        result = sanitize_string("  hello world  ")
        assert result == "hello world"

    def test_removes_angle_brackets(self) -> None:
        """Verify that HTML-like angle brackets are stripped."""
        result = sanitize_string("hello <script>alert</script> world")
        assert "<" not in result
        assert ">" not in result

    def test_removes_shell_injection_chars(self) -> None:
        """Verify that shell injection characters are removed."""
        result = sanitize_string("city; rm -rf /")
        assert ";" not in result

    def test_removes_pipe_characters(self) -> None:
        """Verify that pipe characters used in command chaining are removed."""
        result = sanitize_string("input | cat /etc/passwd")
        assert "|" not in result

    def test_exceeds_max_length_raises_error(self) -> None:
        """Verify ValueError is raised for oversized input."""
        long_input = "a" * 5001
        with pytest.raises(ValueError, match="maximum length"):
            sanitize_string(long_input)

    def test_max_length_boundary_passes(self) -> None:
        """Verify that input at exactly max length is accepted."""
        boundary_input = "a" * 5000
        result = sanitize_string(boundary_input)
        assert len(result) == 5000


class TestValidateLocation:
    """Test suite for the validate_location function."""

    def test_valid_city_name(self) -> None:
        """Verify valid city names pass validation."""
        assert validate_location("New York") is True

    def test_valid_city_with_country(self) -> None:
        """Verify city, country format passes validation."""
        assert validate_location("London, United Kingdom") is True

    def test_valid_hyphenated_name(self) -> None:
        """Verify hyphenated location names pass validation."""
        assert validate_location("Stratford-upon-Avon") is True

    def test_invalid_with_numbers(self) -> None:
        """Verify locations with numbers fail validation."""
        assert validate_location("City123") is False

    def test_invalid_with_special_chars(self) -> None:
        """Verify locations with special characters fail validation."""
        assert validate_location("City<script>") is False

    def test_empty_string_fails(self) -> None:
        """Verify empty string fails validation."""
        assert validate_location("") is False


class TestValidateDate:
    """Test suite for the validate_date function."""

    def test_valid_date(self) -> None:
        """Verify valid ISO date format passes."""
        assert validate_date("2025-03-15") is True

    def test_valid_date_december(self) -> None:
        """Verify December date passes validation."""
        assert validate_date("2025-12-31") is True

    def test_invalid_format_slash(self) -> None:
        """Verify slash-separated date fails validation."""
        assert validate_date("2025/03/15") is False

    def test_invalid_month(self) -> None:
        """Verify month 13 fails validation."""
        assert validate_date("2025-13-01") is False

    def test_invalid_day(self) -> None:
        """Verify day 32 fails validation."""
        assert validate_date("2025-01-32") is False

    def test_empty_string(self) -> None:
        """Verify empty string fails validation."""
        assert validate_date("") is False


class TestValidatePositiveInteger:
    """Test suite for the validate_positive_integer function."""

    def test_positive_integer(self) -> None:
        """Verify positive integer passes validation."""
        assert validate_positive_integer(5) is True

    def test_zero_fails(self) -> None:
        """Verify zero fails validation."""
        assert validate_positive_integer(0) is False

    def test_negative_fails(self) -> None:
        """Verify negative integer fails validation."""
        assert validate_positive_integer(-1) is False

    def test_float_fails(self) -> None:
        """Verify float fails validation."""
        assert validate_positive_integer(1.5) is False

    def test_string_fails(self) -> None:
        """Verify string fails validation."""
        assert validate_positive_integer("5") is False
