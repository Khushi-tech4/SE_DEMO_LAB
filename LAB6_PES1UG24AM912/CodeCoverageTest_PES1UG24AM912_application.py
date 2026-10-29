import pytest

from course_registration import (
    can_register,
    waitlist_position,
    late_fee
)


# Tests for can_register()


def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"


def test_unknown_student_status():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("invalid", 10, 3, True)


def test_invalid_course_credits():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)


def test_negative_course_credits():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, -2, True)


def test_prerequisites_missing():
    assert can_register("regular", 10, 3, False) == "prerequisites missing"


def test_credit_limit_exceeded():
    assert can_register("regular", 22, 4, True) == "credit limit exceeded"


def test_probation_credit_limit():
    assert can_register("probation", 14, 3, True) == "credit limit exceeded"


def test_honors_student_registered():
    assert can_register("honors", 20, 8, True) == "registered"


def test_exact_credit_limit():
    assert can_register("regular", 20, 4, True) == "registered"


# Tests for waitlist_position()


def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0


def test_invalid_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, 0, 2)


def test_negative_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, -5, 2)


def test_waitlist_position():
    assert waitlist_position(40, 40, 3) == 4


def test_waitlist_full():
    assert waitlist_position(40, 40, 10) == -1


def test_waitlist_over_limit():
    assert waitlist_position(40, 40, 12) == -1


# Tests for late_fee()


def test_no_late_fee():
    assert late_fee(0, 15, False) == 0


def test_negative_days_late():
    assert late_fee(-2, 15, False) == 0


def test_fee_waiver():
    assert late_fee(10, 15, True) == 0


def test_late_fee_within_seven_days():
    assert late_fee(5, 15, False) == 500


def test_late_fee_after_seven_days():
    assert late_fee(10, 15, False) == 800


def test_additional_fee_for_more_than_twenty_credits():
    assert late_fee(5, 21, False) == 750


def test_no_additional_fee_at_twenty_credits():
    assert late_fee(5, 20, False) == 500


def test_maximum_late_fee():
    assert late_fee(30, 25, False) == 2000