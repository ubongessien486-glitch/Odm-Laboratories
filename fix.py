import re

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

with open('diagnostic.html', 'r', encoding='utf-8') as f:
    diag_html = f.read()

# Grab Trust Bar to end of Service 1 from index.html
match = re.search(r'(<!-- Trust Bar -->.*?<!-- Service 2 -->)', index_html, re.DOTALL)
if match:
    extracted = match.group(1)
    
    # In diagnostic.html, find where it ends the hero section:
    # </a>\s*<a href="about.html" class="btn-outline">Learn More</a>\s*</div>\s*</div>\s*</section>
    hero_end = re.search(r'</section>', diag_html)
    service_2 = re.search(r'<!-- Service 2 -->', diag_html)
    
    if hero_end and service_2:
        new_diag = diag_html[:hero_end.end()] + "\n\n" + extracted + diag_html[service_2.end():]
        
        # Remove CLIA
        new_diag = re.sub(r'<img[^>]*src="clia-certified\.png"[^>]*>', '', new_diag)
        
        with open('diagnostic.html', 'w', encoding='utf-8') as out:
            out.write(new_diag)
        print("Success")
    else:
        print("Could not find insertion points")
