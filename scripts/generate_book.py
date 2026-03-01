import os
import re
import yaml
import sys

def parse_readme(content):
    """Parse README content to extract project titles and descriptions."""
    # Split by headings
    sections = re.split(r'^###\s+', content, flags=re.MULTILINE)

    projects = []

    for section in sections:
        lines = section.splitlines()
        if not lines:
            continue

        title = lines[0].strip()
        body = "\n".join(lines[1:])

        # Remove HTML comments to avoid matching templates
        body_no_comments = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)

        # Check if it's a project section
        is_project = "**Suggested Language**:" in body_no_comments or "**Suggested Frameworks/Tools**:" in body_no_comments

        if is_project:
            # Extract description
            match = re.search(r'(.*?)\*\*Suggested Language\*\*:', body_no_comments, re.DOTALL)
            if match:
                description = match.group(1).strip()
            else:
                 match = re.search(r'(.*?)\*\*Suggested Frameworks/Tools\*\*:', body_no_comments, re.DOTALL)
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
    """Create a filesystem-safe filename from a title."""
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
    safe_title = re.sub(r'[-\s]+', '-', safe_title)
    return f"{safe_title}.qmd"

def generate_qmd_content(title, description, filename):
    """Generate the content for a .qmd file."""
    safe_title = filename.replace('.qmd', '')
    function_name = safe_title.replace('-', '_')
    if function_name and function_name[0].isdigit():
         function_name = f"project_{function_name}"

    return f"""---
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

def update_quarto_config(quarto_yml_path, chapter_filenames):
    """Update _quarto.yml with the list of generated chapters."""
    if os.path.exists(quarto_yml_path):
        with open(quarto_yml_path, "r", encoding="utf-8") as f:
            quarto_config = yaml.safe_load(f)
    else:
        quarto_config = {}

    if "book" not in quarto_config:
        quarto_config["book"] = {}

    # Define standard chapters
    default_chapters = ["index.qmd", "intro.qmd", "summary.qmd", "references.qmd"]

    # Merge existing with new
    new_chapter_list = [c for c in default_chapters]
    seen_chapters = set(new_chapter_list)

    # Add generated chapters
    for filename in chapter_filenames:
        if filename not in seen_chapters:
            new_chapter_list.append(filename)
            seen_chapters.add(filename)

    quarto_config["book"]["chapters"] = new_chapter_list

    with open(quarto_yml_path, "w", encoding="utf-8") as f:
        yaml.dump(quarto_config, f, sort_keys=False, allow_unicode=True)

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
        filename = sanitize_filename(project["title"])
        filepath = os.path.join(output_dir, filename)
        chapter_filenames.append(filename)

        qmd_content = generate_qmd_content(project["title"], project["description"], filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(qmd_content)

    print(f"Generated {len(chapter_filenames)} .qmd files.")

    quarto_yml_path = os.path.join(output_dir, "_quarto.yml")
    update_quarto_config(quarto_yml_path, chapter_filenames)
    print("Updated _quarto.yml")

if __name__ == "__main__":
    main()
