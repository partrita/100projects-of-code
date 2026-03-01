import os
import re
import yaml
import sys

def parse_readme(content):
    # Split by headings
    sections = re.split(r'^###\s+', content, flags=re.MULTILINE)

    projects = []

    # Support both English and Korean markers
    lang_markers = [r'\*\*Suggested Language\*\*:', r'\*\*권장 언어\*\*:']
    framework_markers = [r'\*\*Suggested Frameworks/Tools\*\*:', r'\*\*권장 프레임워크/도구\*\*:']

    combined_markers = lang_markers + framework_markers
    marker_pattern = '|'.join(combined_markers)

    for section in sections:
        lines = section.splitlines()
        if not lines:
            continue

        title = lines[0].strip()
        body = "\n".join(lines[1:])

        # Remove HTML comments to avoid matching templates
        body_no_comments = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)

        # Check if it's a project section
        is_project = any(re.search(marker, body_no_comments) for marker in combined_markers)

        if is_project:
            # Extract description
            match = re.search(f'(.*?)(?:{marker_pattern})', body_no_comments, re.DOTALL)
            if match:
                description = match.group(1).strip()
            else:
                description = body_no_comments.strip() # Fallback

            projects.append({
                "title": title,
                "description": description
            })
    return projects

def sanitize_filename(title):
    # Create sanitized filename
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
    safe_title = re.sub(r'[-\s]+', '-', safe_title)
    return safe_title

def generate_qmd_content(title, description, safe_title):
    function_name = safe_title.replace('-', '_')
    if function_name and function_name[0].isdigit():
         function_name = f"project_{function_name}"
    elif not function_name:
         function_name = "project"

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
    return content

def update_quarto_config(quarto_config, chapter_filenames):
    if "book" not in quarto_config:
        quarto_config["book"] = {}

    # Define standard chapters
    default_chapters = ["index.qmd", "intro.qmd", "summary.qmd", "references.qmd"]

    # Merge existing with new
    new_chapter_list = [c for c in default_chapters]

    # Add generated chapters
    for filename in chapter_filenames:
        if filename not in new_chapter_list:
            new_chapter_list.append(filename)

    quarto_config["book"]["chapters"] = new_chapter_list
    return quarto_config

def main():
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("README.md not found!")
        sys.exit(1)

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    projects = parse_readme(content)

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
        safe_title = sanitize_filename(title)
        filename = f"{safe_title}.qmd"
        filepath = os.path.join(output_dir, filename)

        chapter_filenames.append(filename)

        qmd_content = generate_qmd_content(title, description, safe_title)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(qmd_content)

    print(f"Generated {len(chapter_filenames)} .qmd files.")

    # Update _quarto.yml
    quarto_yml_path = os.path.join(output_dir, "_quarto.yml")
    if os.path.exists(quarto_yml_path):
        with open(quarto_yml_path, "r", encoding="utf-8") as f:
            quarto_config = yaml.safe_load(f)
    else:
        quarto_config = {}

    updated_config = update_quarto_config(quarto_config, chapter_filenames)

    with open(quarto_yml_path, "w", encoding="utf-8") as f:
        yaml.dump(updated_config, f, sort_keys=False, allow_unicode=True)

    print("Updated _quarto.yml")

if __name__ == "__main__":
    main()
