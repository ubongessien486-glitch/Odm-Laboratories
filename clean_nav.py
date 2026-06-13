import os

for root, _, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            new_lines = []
            in_desktop_nav = False
            in_mobile_nav = False
            modified = False
            
            for line in lines:
                if '<ul class="nav-links">' in line:
                    in_desktop_nav = True
                elif '</ul>' in line and in_desktop_nav:
                    in_desktop_nav = False
                
                if '<div class="mobile-menu"' in line:
                    in_mobile_nav = True
                elif '</div>' in line and in_mobile_nav:
                    in_mobile_nav = False
                
                # If we are in nav menus, strip existing employment testing links completely
                if (in_desktop_nav or in_mobile_nav) and 'employment-testing.html' in line and 'Employment Testing' in line:
                    modified = True
                    continue # Skip this line to remove it
                
                # Now, add EXACTLY ONE when we hit 'about.html'
                if in_desktop_nav and 'href="about.html"' in line and 'About Us' in line:
                    indent = line[:line.find('<')]
                    new_lines.append(indent + '<li><a href="employment-testing.html">Employment Testing</a></li>\n')
                    modified = True
                
                if in_mobile_nav and 'href="about.html"' in line and 'About Us' in line:
                    indent = line[:line.find('<')]
                    new_lines.append(indent + '<a href="employment-testing.html">Employment Testing</a>\n')
                    modified = True
                
                new_lines.append(line)
            
            if modified:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.writelines(new_lines)
