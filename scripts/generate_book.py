import os
import re
import yaml
import sys

# Pre-compiled regex patterns for performance
RE_HEADING = re.compile(r'^###\s+', re.MULTILINE)
RE_HTML_COMMENT = re.compile(r'<!--.*?-->', re.DOTALL)
RE_SAFE_TITLE = re.compile(r'[^\w\s-]')
RE_DASHES = re.compile(r'[-\s]+')

# Project detection patterns
RE_PROJECT_MARKERS = [
    re.compile(r'(.*?)\*\*Suggested Language\*\*:', re.DOTALL),
    re.compile(r'(.*?)\*\*Suggested Frameworks/Tools\*\*:', re.DOTALL),
    re.compile(r'(.*?)\*\*권장 언어\*\*:', re.DOTALL),
    re.compile(r'(.*?)\*\*권장 프레임워크/도구\*\*:', re.DOTALL),
]

def main():
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("README.md not found!")
        sys.exit(1)

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by headings
    sections = RE_HEADING.split(content)

    projects = []

    for section in sections:
        lines = section.splitlines()
        if not lines:
            continue

        title = lines[0].strip()
        body = "\n".join(lines[1:])

        # Remove HTML comments to avoid matching templates
        body_no_comments = RE_HTML_COMMENT.sub('', body)

        # Check for English or Korean project markers
        description = None
        for pattern in RE_PROJECT_MARKERS:
            match = pattern.search(body_no_comments)
            if match:
                description = match.group(1).strip()
                break

        if description is not None:
            projects.append({
                "title": title,
                "description": description
            })

    print(f"Found {len(projects)} projects.")

    if not projects:
        print("No projects found! Check parsing logic.")
        sys.exit(1)

    output_dir = "mybook"
    os.makedirs(output_dir, exist_ok=True)

    chapter_filenames = []

    for project in projects:
        title = project["title"]
        description = project["description"]

        # Create sanitized filename
        safe_title = RE_SAFE_TITLE.sub('', title).strip().lower()
        safe_title = RE_DASHES.sub('-', safe_title)
        filename = f"{safe_title}.qmd"
        filepath = os.path.join(output_dir, filename)

        chapter_filenames.append(filename)

        # Generate content
        function_name = safe_title.replace('-', '_')
        if function_name and function_name[0].isdigit():
            function_name = f"project_{function_name}"

        content = f"""---
title: "{title}"
---

{description}

## Python Implementation

```python
def {function_name}():
    \"\"\"
    Implementation for {title}
    \"\"\"
    print("Executing {title}...")
    # TODO: Add your implementation here
    pass

if __name__ == "__main__":
    {function_name}()
```
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Generated {len(chapter_filenames)} .qmd files.")

    # Update _quarto.yml
    quarto_yml_path = os.path.join(output_dir, "_quarto.yml")
    if os.path.exists(quarto_yml_path):
        with open(quarto_yml_path, "r", encoding="utf-8") as f:
            quarto_config = yaml.safe_load(f) or {}
    else:
        quarto_config = {}

    if "book" not in quarto_config:
        quarto_config["book"] = {}

    existing_chapters = quarto_config["book"].get("chapters", [])

    # Define standard chapters
    default_chapters = ["index.qmd", "intro.qmd", "summary.qmd", "references.qmd"]

    # Merge while maintaining order and ensuring O(1) membership check
    new_chapter_list = []
    seen_chapters = set()

    for chapter in default_chapters + existing_chapters + chapter_filenames:
        if chapter not in seen_chapters:
            new_chapter_list.append(chapter)
            seen_chapters.add(chapter)

    quarto_config["book"]["chapters"] = new_chapter_list

    with open(quarto_yml_path, "w", encoding="utf-8") as f:
        yaml.dump(quarto_config, f, sort_keys=False, allow_unicode=True)

    print("Updated _quarto.yml")

if __name__ == "__main__":
    main()
