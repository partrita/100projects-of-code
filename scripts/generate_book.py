import os
import re
import yaml
import sys

def main():
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("README.md not found!")
        sys.exit(1)

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

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

            # Clean up title
            # Remove any trailing anchor links if present in the title line (uncommon in ### but possible)
            # The regex for split consumed the ###

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

    # Pre-compile regex patterns for title sanitization
    re_sanitize = re.compile(r'[^\w\s-]')
    re_dashes_spaces = re.compile(r'[-\s]+')

    for project in projects:
        title = project["title"]
        description = project["description"]

        # Create sanitized filename
        safe_title = re_sanitize.sub('', title).strip().lower()
        safe_title = re_dashes_spaces.sub('-', safe_title)
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
