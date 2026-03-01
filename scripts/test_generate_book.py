import pytest
from scripts.generate_book import parse_projects

def test_parse_projects_english():
    content = """
### Project 1

Description 1

**Suggested Language**: Python
**Suggested Frameworks/Tools**: Flask

### Project 2

Description 2

**Suggested Frameworks/Tools**: Django
"""
    projects = parse_projects(content)
    assert len(projects) == 2
    assert projects[0]["title"] == "Project 1"
    assert projects[0]["description"] == "Description 1"
    assert projects[1]["title"] == "Project 2"
    assert projects[1]["description"] == "Description 2"

def test_parse_projects_korean():
    content = """
### 프로젝트 1

설명 1

**권장 언어**: Python
**권장 프레임워크/도구**: Flask
"""
    # Current implementation should fail this test because it doesn't support Korean markers yet
    projects = parse_projects(content)
    assert len(projects) == 1
    assert projects[0]["title"] == "프로젝트 1"
    assert projects[0]["description"] == "설명 1"

def test_parse_projects_no_projects():
    content = """
### Not a project

Just some text without suggested language or tools.
"""
    projects = parse_projects(content)
    assert len(projects) == 0

def test_parse_projects_with_comments():
    content = """
### Real Project

Real description

**Suggested Language**: Java

### Template <!--

### Not a Project

**Suggested Language**: None
-->
"""
    projects = parse_projects(content)
    assert len(projects) == 1
    assert projects[0]["title"] == "Real Project"

def test_parse_projects_empty():
    assert parse_projects("") == []
