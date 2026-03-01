import unittest.mock as mock
import pytest
import sys
import os
from scripts.generate_book import main

def test_main_readme_not_found():
    # Patch the functions directly in the module they are used
    with mock.patch("scripts.generate_book.os.path.exists") as mock_exists:
        # Mock os.path.exists to return False for README.md
        mock_exists.side_effect = lambda path: False if path == "README.md" else True

        with mock.patch("scripts.generate_book.sys.exit") as mock_exit:
            # We expect sys.exit to be called
            mock_exit.side_effect = SystemExit(1)

            with pytest.raises(SystemExit) as excinfo:
                main()

            assert excinfo.value.code == 1
            mock_exit.assert_called_with(1)

def test_main_happy_path():
    readme_content = """
### Project Title
Description of the project.
**Suggested Language**: Python
"""
    # Patch everything to avoid side effects
    with mock.patch("scripts.generate_book.os.path.exists") as mock_exists, \
         mock.patch("scripts.generate_book.open", mock.mock_open(read_data=readme_content)) as mock_file, \
         mock.patch("scripts.generate_book.os.makedirs") as mock_makedirs, \
         mock.patch("scripts.generate_book.yaml.safe_load") as mock_yaml_load, \
         mock.patch("scripts.generate_book.yaml.dump") as mock_yaml_dump:

        # Mock os.path.exists to return True for everything except _quarto.yml
        mock_exists.side_effect = lambda path: False if path.endswith("_quarto.yml") else True
        mock_yaml_load.return_value = {"book": {"chapters": []}}

        # Ensure sys.exit is not called with 1
        with mock.patch("scripts.generate_book.sys.exit") as mock_exit:
            main()
            for call in mock_exit.call_args_list:
                assert call[0][0] != 1

        # Verify that it tried to write the qmd file
        mock_file.assert_any_call(os.path.join("mybook", "project-title.qmd"), "w", encoding="utf-8")
        # Verify that it tried to update _quarto.yml
        mock_file.assert_any_call(os.path.join("mybook", "_quarto.yml"), "w", encoding="utf-8")
