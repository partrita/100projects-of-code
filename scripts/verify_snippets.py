import os
import subprocess
import re

def extract_python_blocks(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple regex to find python code blocks
    blocks = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)
    return blocks

def main():
    files_to_check = [
        "mybook/twitter-bot.qmd",
        "mybook/messenger-bot.qmd",
        "mybook/news-aggregator.qmd",
        "mybook/slack-bot.qmd",
        "mybook/traffic-notifier.qmd",
        "mybook/weather-app.qmd"
    ]

    for filepath in files_to_check:
        print(f"Checking {filepath}...")
        blocks = extract_python_blocks(filepath)
        for i, block in enumerate(blocks):
            temp_filename = f"temp_{os.path.basename(filepath)}_{i}.py"
            with open(temp_filename, 'w', encoding='utf-8') as f:
                f.write(block)

            try:
                subprocess.run(['python', '-m', 'py_compile', temp_filename], check=True)
                print(f"  Block {i}: Syntax OK")
            except subprocess.CalledProcessError:
                print(f"  Block {i}: Syntax ERROR")
            finally:
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)

if __name__ == "__main__":
    main()
