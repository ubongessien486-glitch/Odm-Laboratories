import os

for root, _, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Replace wrong phone numbers in all files
            content = content.replace('(219) 306-0674', '312-772-3381 / 779-236-7071')
            content = content.replace('((219) 306-0674', '312-772-3381 / 779-236-7071')
            content = content.replace('tel:+12193060674', 'tel:312-772-3381')

            # Add navigation links
            content = content.replace(
                '<li><a href="employment-testing.html">Employment Testing</a></li>',
                '<li><a href="employment-testing.html">Employment Testing</a></li>\n                        <li><a href="drug-free-workplace.html">Non-DOT Drug Testing</a></li>'
            )
            content = content.replace(
                '<a href="employment-testing.html">Employment Testing</a>\n          <a href="about.html">',
                '<a href="employment-testing.html">Employment Testing</a>\n          <a href="drug-free-workplace.html">Non-DOT Drug Testing</a>\n          <a href="about.html">'
            )
            
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
