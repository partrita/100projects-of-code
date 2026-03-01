import re

# Same patterns as in generate_book.py
RE_HTML_COMMENT = re.compile(r'<!--.*?-->', re.DOTALL)
RE_SUGGESTED_LANG = re.compile(r'(.*?)\*\*Suggested Language\*\*:', re.DOTALL)
RE_SUGGESTED_TOOLS = re.compile(r'(.*?)\*\*Suggested Frameworks/Tools\*\*:', re.DOTALL)
RE_INVALID_TITLE_CHARS = re.compile(r'[^\w\s-]')
RE_DASHES_SPACES = re.compile(r'[-\s]+')

def test_logic():
    # Test HTML comment removal
    body = "text <!-- comment --> more text"
    assert RE_HTML_COMMENT.sub('', body) == "text  more text"

    # Test project description extraction (Language)
    body_no_comments = "Project description\n**Suggested Language**: Python"
    match = RE_SUGGESTED_LANG.search(body_no_comments)
    assert match.group(1).strip() == "Project description"

    # Test project description extraction (Tools)
    body_no_comments = "Another description\n**Suggested Frameworks/Tools**: Flask"
    match = RE_SUGGESTED_TOOLS.search(body_no_comments)
    assert match.group(1).strip() == "Another description"

    # Test filename sanitization
    title = "My Project! @2023"
    safe_title = RE_INVALID_TITLE_CHARS.sub('', title).strip().lower()
    assert safe_title == "my project 2023"
    safe_title = RE_DASHES_SPACES.sub('-', safe_title)
    assert safe_title == "my-project-2023"

    print("All regex logic tests passed!")

if __name__ == "__main__":
    test_logic()
