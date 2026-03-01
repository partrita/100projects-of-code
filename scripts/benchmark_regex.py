import re
import timeit

# Sample data similar to what might be in the README
sample_body = """
This is a project description.
<!--
This is a comment that should be removed.
It spans multiple lines.
-->
**Suggested Language**: Python
**Suggested Frameworks/Tools**: Flask
""" * 10  # Make it a bit larger

def without_precompilation():
    body = sample_body
    for _ in range(1000):
        body_no_comments = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)

# Pre-compile outside
comment_re = re.compile(r'<!--.*?-->', flags=re.DOTALL)

def with_precompilation():
    body = sample_body
    for _ in range(1000):
        body_no_comments = comment_re.sub('', body)

if __name__ == "__main__":
    t1 = timeit.timeit(without_precompilation, number=100)
    t2 = timeit.timeit(with_precompilation, number=100)

    print(f"Without pre-compilation: {t1:.4f}s")
    print(f"With pre-compilation:    {t2:.4f}s")
    print(f"Improvement: {(t1 - t2) / t1 * 100:.2f}%")
