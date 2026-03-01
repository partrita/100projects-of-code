import pytest
from scripts.generate_book import parse_readme, sanitize_filename

def test_parse_readme_english():
    content = """
### Project 1
This is a description.
**Suggested Language**: Python
"""
    projects = parse_readme(content)
    assert len(projects) == 1
    assert projects[0]['title'] == "Project 1"
    assert projects[0]['description'] == "This is a description."

def test_parse_readme_korean():
    content = """
### 프로젝트 1
설명입니다.
**권장 언어**: 파이썬
"""
    projects = parse_readme(content)
    assert len(projects) == 1
    assert projects[0]['title'] == "프로젝트 1"
    assert projects[0]['description'] == "설명입니다."

def test_parse_readme_mixed():
    content = """
### Project 1
English description.
**Suggested Frameworks/Tools**: Flask

### 프로젝트 2
한국어 설명.
**권장 프레임워크/도구**: Django
"""
    projects = parse_readme(content)
    assert len(projects) == 2
    assert projects[0]['title'] == "Project 1"
    assert projects[1]['title'] == "프로젝트 2"

def test_parse_readme_ignore_comments():
    content = """
<!--
### Template
Template description.
**Suggested Language**: Python
-->

### Actual Project
Real description.
**Suggested Language**: Python
"""
    projects = parse_readme(content)
    assert len(projects) == 1
    assert projects[0]['title'] == "Actual Project"

def test_parse_readme_no_projects():
    content = """
# Title
## Introduction
Some text without projects.
"""
    projects = parse_readme(content)
    assert len(projects) == 0

def test_sanitize_filename():
    assert sanitize_filename("Simple Title") == "simple-title.qmd"
    assert sanitize_filename("Title with! Special@ Characters#") == "title-with-special-characters.qmd"
    assert sanitize_filename("   Spaces and---Dashes   ") == "spaces-and-dashes.qmd"
    assert sanitize_filename("한글 제목") == "한글-제목.qmd"
