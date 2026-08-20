from employee.utils.parse_ids import parse_ids


def test_parse_ids_converts_the_post_list_of_strings():
    # This is the real shape of the input: request.POST.getlist(...).
    assert parse_ids(["1", "2", "3"]) == [1, 2, 3]


def test_parse_ids_preserves_order_and_duplicates():
    assert parse_ids(["3", "1", "3"]) == [3, 1, 3]


def test_parse_ids_returns_empty_for_an_empty_list():
    # Callers rely on this to short-circuit "nothing was checked" before
    # touching the queryset — an empty list must never mean "all rows".
    assert parse_ids([]) == []


def test_parse_ids_skips_unconvertible_entries_instead_of_raising():
    assert parse_ids(["1", "abc", "", None, "2"]) == [1, 2]


def test_parse_ids_tolerates_padded_numbers():
    assert parse_ids([" 7 ", "007"]) == [7, 7]


def test_parse_ids_handles_floats_inconsistently():
    # int("3.9") raises and the entry is dropped, but int(3.9) truncates —
    # so the same value survives or vanishes depending on whether it arrived
    # as form data or as an already-decoded number.
    assert parse_ids(["3.9"]) == []
    assert parse_ids([3.9]) == [3]


def test_parse_ids_does_not_reject_negative_or_zero_ids():
    # No range guard here; the queryset filter is what ends up rejecting them.
    assert parse_ids(["-1", "0"]) == [-1, 0]


def test_parse_ids_turns_booleans_into_ids():
    assert parse_ids([True, False]) == [1, 0]


def test_parse_ids_explodes_a_bare_string_into_digits():
    # getlist() always returns a list, but a caller that hands over a single
    # id string gets it iterated character by character — three bogus ids
    # instead of one real one, with no error to notice.
    assert parse_ids("123") == [1, 2, 3]
