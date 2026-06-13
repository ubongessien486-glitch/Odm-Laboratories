import glob
import re

html_files = glob.glob('*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace anything like styles.css?v=... with styles.css?v=3104
    new_content = re.sub(r'styles\.css\?v=\w+', 'styles.css?v=3104', content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated cache buster in {filepath}")

print("Done updating HTML cache busters.")
