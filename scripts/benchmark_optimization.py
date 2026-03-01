import timeit
import random
import string

def current_implementation(chapter_filenames, new_chapter_list):
    for filename in chapter_filenames:
        if filename not in new_chapter_list:
            new_chapter_list.append(filename)
    return new_chapter_list

def optimized_implementation(chapter_filenames, new_chapter_list):
    seen = set(new_chapter_list)
    for filename in chapter_filenames:
        if filename not in seen:
            new_chapter_list.append(filename)
            seen.add(filename)
    return new_chapter_list

def generate_data(num_existing, num_new):
    existing = ["".join(random.choices(string.ascii_lowercase, k=10)) + ".qmd" for _ in range(num_existing)]
    new_files = ["".join(random.choices(string.ascii_lowercase, k=10)) + ".qmd" for _ in range(num_new)]
    # Add some overlaps
    new_files.extend(random.choices(existing, k=num_new // 10))
    random.shuffle(new_files)
    return existing, new_files

def benchmark():
    num_existing = 1000
    num_new = 5000

    existing, new_files = generate_data(num_existing, num_new)

    # Verify correctness
    res1 = current_implementation(new_files[:], existing[:])
    res2 = optimized_implementation(new_files[:], existing[:])
    assert res1 == res2
    print("Verification successful: Both implementations yield the same result.")

    t1 = timeit.timeit(lambda: current_implementation(new_files[:], existing[:]), number=10)
    t2 = timeit.timeit(lambda: optimized_implementation(new_files[:], existing[:]), number=10)

    print(f"Current implementation: {t1:.6f} seconds (average of 10 runs)")
    print(f"Optimized implementation: {t2:.6f} seconds (average of 10 runs)")
    print(f"Improvement: {(t1 - t2) / t1 * 100:.2f}%")

if __name__ == "__main__":
    benchmark()
