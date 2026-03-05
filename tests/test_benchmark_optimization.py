import pytest
from scripts.benchmark_optimization import current_implementation, optimized_implementation

def test_basic_append():
    existing = ["index.qmd", "intro.qmd"]
    new_files = ["chapter1.qmd", "chapter2.qmd"]

    # Test current
    res_current = current_implementation(new_files, existing[:])
    assert res_current == ["index.qmd", "intro.qmd", "chapter1.qmd", "chapter2.qmd"]

    # Test optimized
    res_optimized = optimized_implementation(new_files, existing[:])
    assert res_optimized == ["index.qmd", "intro.qmd", "chapter1.qmd", "chapter2.qmd"]

def test_duplicates_in_new():
    existing = ["index.qmd"]
    new_files = ["chapter1.qmd", "chapter1.qmd", "chapter2.qmd", "chapter1.qmd"]

    expected = ["index.qmd", "chapter1.qmd", "chapter2.qmd"]

    assert current_implementation(new_files, existing[:]) == expected
    assert optimized_implementation(new_files, existing[:]) == expected

def test_existing_files():
    existing = ["index.qmd", "intro.qmd"]
    new_files = ["intro.qmd", "chapter1.qmd", "index.qmd"]

    expected = ["index.qmd", "intro.qmd", "chapter1.qmd"]

    assert current_implementation(new_files, existing[:]) == expected
    assert optimized_implementation(new_files, existing[:]) == expected

def test_empty_existing():
    existing = []
    new_files = ["chapter1.qmd", "chapter2.qmd", "chapter1.qmd"]

    expected = ["chapter1.qmd", "chapter2.qmd"]

    assert current_implementation(new_files, existing[:]) == expected
    assert optimized_implementation(new_files, existing[:]) == expected

def test_empty_new():
    existing = ["index.qmd", "intro.qmd"]
    new_files = []

    expected = ["index.qmd", "intro.qmd"]

    assert current_implementation(new_files, existing[:]) == expected
    assert optimized_implementation(new_files, existing[:]) == expected

def test_order_preserved():
    existing = ["z.qmd", "a.qmd"]
    new_files = ["c.qmd", "b.qmd", "d.qmd"]

    expected = ["z.qmd", "a.qmd", "c.qmd", "b.qmd", "d.qmd"]

    assert current_implementation(new_files, existing[:]) == expected
    assert optimized_implementation(new_files, existing[:]) == expected

def test_both_match_large_random():
    import random
    import string

    for _ in range(5):
        existing = ["".join(random.choices(string.ascii_lowercase, k=5)) for _ in range(50)]
        new_files = ["".join(random.choices(string.ascii_lowercase, k=5)) for _ in range(200)]

        # Add some known overlaps
        new_files.extend(random.choices(existing, k=20))
        random.shuffle(new_files)

        res1 = current_implementation(new_files, existing[:])
        res2 = optimized_implementation(new_files, existing[:])

        assert res1 == res2
