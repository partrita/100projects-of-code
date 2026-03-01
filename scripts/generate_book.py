import os
import re
import sys

def parse_projects(content):
    # Remove HTML comments to avoid matching templates or commented out sections
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
        # Support both English and Korean markers
        suggested_lang_markers = ["**Suggested Language**:", "**권장 언어**:"]
        suggested_tool_markers = ["**Suggested Frameworks/Tools**:", "**권장 프레임워크/도구**:"]

        is_project = any(marker in body for marker in suggested_lang_markers + suggested_tool_markers)

        if is_project:
            # Extract description
            # Find the first marker to extract description before it
            all_markers = suggested_lang_markers + suggested_tool_markers
            # Create a regex to match any of the markers
            marker_regex = '|'.join(re.escape(m) for m in all_markers)
            match = re.search(f'(.*?)(?:{marker_regex})', body, re.DOTALL)

            if match:
                description = match.group(1).strip()
            else:
                description = body.strip() # Fallback

            projects.append({
                "title": title,
                "description": description
            })
    return projects

def main():
    import yaml
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("README.md not found!")
        sys.exit(1)

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    projects = parse_projects(content)

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
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        filename = f"{safe_title}.qmd"
        filepath = os.path.join(output_dir, filename)

        chapter_filenames.append(filename)

        # Generate content
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
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Generated {len(chapter_filenames)} .qmd files.")

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

    # Define standard chapters
    default_chapters = ["index.qmd", "intro.qmd", "summary.qmd", "references.qmd"]

    # Merge existing (from create project) with new
    # Start with defaults
    new_chapter_list = [c for c in default_chapters]

    # Add generated chapters
    for filename in chapter_filenames:
        if filename not in new_chapter_list:
            new_chapter_list.append(filename)

    quarto_config["book"]["chapters"] = new_chapter_list

    with open(quarto_yml_path, "w", encoding="utf-8") as f:
        yaml.dump(quarto_config, f, sort_keys=False, allow_unicode=True)

    print("Updated _quarto.yml")

if __name__ == "__main__":
    main()
