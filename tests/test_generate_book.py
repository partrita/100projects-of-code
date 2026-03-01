import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add scripts directory to path to import generate_book
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Mock yaml before importing generate_book if it's not available
try:
    import yaml
except ImportError:
    mock_yaml = MagicMock()
    sys.modules['yaml'] = mock_yaml

import generate_book

class TestGenerateBook(unittest.TestCase):

    def test_parse_readme_english(self):
        content = """
### Project English
This is a description.
**Suggested Language**: Python
"""
        projects = generate_book.parse_readme(content)
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]['title'], 'Project English')
        self.assertEqual(projects[0]['description'], 'This is a description.')

    def test_parse_readme_korean(self):
        content = """
### 프로젝트 한국어
이것은 설명입니다.
**권장 언어**: Python
"""
        projects = generate_book.parse_readme(content)
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]['title'], '프로젝트 한국어')
        self.assertEqual(projects[0]['description'], '이것은 설명입니다.')

    def test_parse_readme_no_projects(self):
        content = """
### Not a Project
This section doesn't have the markers.
"""
        projects = generate_book.parse_readme(content)
        self.assertEqual(len(projects), 0)

    def test_sanitize_filename(self):
        self.assertEqual(generate_book.sanitize_filename("Hello World!"), "hello-world")
        self.assertEqual(generate_book.sanitize_filename("Project #1"), "project-1")
        self.assertEqual(generate_book.sanitize_filename("  Spaces  "), "spaces")

    def test_generate_qmd_content(self):
        title = "My Project"
        description = "Description"
        safe_title = "my-project"
        content = generate_book.generate_qmd_content(title, description, safe_title)
        self.assertIn('title: "My Project"', content)
        self.assertIn('Description', content)
        self.assertIn('def my_project():', content)

    def test_generate_qmd_content_numeric_start(self):
        title = "100 Projects"
        description = "Description"
        safe_title = "100-projects"
        content = generate_book.generate_qmd_content(title, description, safe_title)
        self.assertIn('def project_100_projects():', content)

    def test_update_quarto_config(self):
        config = {"book": {"chapters": ["index.qmd"]}}
        chapters = ["project1.qmd", "project2.qmd"]
        updated = generate_book.update_quarto_config(config, chapters)

        expected_chapters = ["index.qmd", "intro.qmd", "summary.qmd", "references.qmd", "project1.qmd", "project2.qmd"]
        self.assertEqual(updated['book']['chapters'], expected_chapters)

if __name__ == '__main__':
    unittest.main()
