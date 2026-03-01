import os
import re
import yaml
import sys

def parse_readme(content):
    # Remove HTML comments to avoid matching templates
    content_no_comments = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # Split by headings
    sections = re.split(r'^###\s+', content_no_comments, flags=re.MULTILINE)

    projects = []

    for section in sections:
        lines = section.splitlines()
        if not lines:
            continue

        title = lines[0].strip()
        body = "\n".join(lines[1:])

        # Check if it's a project section
        is_project = (
            "**Suggested Language**:" in body or
            "**Suggested Frameworks/Tools**:" in body or
            "**권장 언어**:" in body or
            "**권장 프레임워크/도구**:" in body
        )

        if is_project:
            # Extract description
            # Try English markers
            match = re.search(r'(.*?)\*\*Suggested (?:Language|Frameworks/Tools)\*\*:', body, re.DOTALL)
            if not match:
                # Try Korean markers
                match = re.search(r'(.*?)\*\*권장 (?:언어|프레임워크/도구)\*\*:', body, re.DOTALL)

            if match:
                description = match.group(1).strip()
            else:
                description = body.strip() # Fallback

            projects.append({
                "title": title,
                "description": description
            })
    return projects

def sanitize_filename(title):
    # Create sanitized filename
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
    safe_title = re.sub(r'[-\s]+', '-', safe_title)
    return f"{safe_title}.qmd"

def generate_qmd_content(title, description):
    filename = sanitize_filename(title)
    safe_title = filename.replace('.qmd', '')
    function_name = safe_title.replace('-', '_')
    if function_name[0].isdigit():
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
    return content

def update_quarto_config(output_dir, chapter_filenames):
    # Update _quarto.yml
    quarto_yml_path = os.path.join(output_dir, "_quarto.yml")
    if os.path.exists(quarto_yml_path):
        with open(quarto_yml_path, "r", encoding="utf-8") as f:
            quarto_config = yaml.safe_load(f)
    else:
        quarto_config = {}

    if "book" not in quarto_config:
        quarto_config["book"] = {}

    existing_chapters = quarto_config["book"].get("chapters", [])

    # Start with existing chapters if they exist, otherwise use a default list
    if existing_chapters:
        new_chapter_list = list(existing_chapters)
    else:
        new_chapter_list = ["index.qmd", "intro.qmd", "summary.qmd", "references.qmd"]

    seen_chapters = set(new_chapter_list)

    # Add generated chapters
    for filename in chapter_filenames:
        if filename not in seen_chapters:
            new_chapter_list.append(filename)
            seen_chapters.add(filename)

    quarto_config["book"]["chapters"] = new_chapter_list

    with open(quarto_yml_path, "w", encoding="utf-8") as f:
        yaml.dump(quarto_config, f, sort_keys=False, allow_unicode=True)

    return quarto_yml_path

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

        filename = sanitize_filename(title)
        filepath = os.path.join(output_dir, filename)
        chapter_filenames.append(filename)

        content = generate_qmd_content(title, description)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Generated {len(chapter_filenames)} .qmd files.")

    quarto_yml_path = update_quarto_config(output_dir, chapter_filenames)
    print(f"Updated {quarto_yml_path}")

if __name__ == "__main__":
    main()
