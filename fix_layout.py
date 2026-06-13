import re

def fix_nested_links(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to change the outer <a class="pillar-card ..."> to <div class="pillar-card ...">
    # And change the closing </a> to </div>
    # And change the <span class="pillar-button"> to <a class="pillar-button" href="...">
    
    # Pillar 1
    content = content.replace(
        '<a href="diagnostic.html" class="pillar-card pillar-card--lab" aria-label="Enter Oxygen Diagnostic Lab">',
        '<div class="pillar-card pillar-card--lab" aria-label="Oxygen Diagnostic Lab">'
    )
    content = content.replace(
        '<span class="pillar-button">Enter Diagnostic Lab <span aria-hidden="true">-&gt;</span></span>\n                    </a>',
        '<a href="diagnostic.html" class="pillar-button" style="text-decoration:none;">Enter Diagnostic Lab <span aria-hidden="true">-&gt;</span></a>\n                    </div>'
    )
    
    # Pillar 2
    content = content.replace(
        '<a href="homecare.html" class="pillar-card pillar-card--home" aria-label="Enter Oxygen Home Care Agency">',
        '<div class="pillar-card pillar-card--home" aria-label="Oxygen Home Care Agency">'
    )
    content = content.replace(
        '<span class="pillar-button">Enter Home Care <span aria-hidden="true">-&gt;</span></span>\n                    </a>',
        '<a href="homecare.html" class="pillar-button" style="text-decoration:none;">Enter Home Care <span aria-hidden="true">-&gt;</span></a>\n                    </div>'
    )
    
    # Pillar 3
    content = content.replace(
        '<a href="login.html" class="pillar-card pillar-card--learn" aria-label="Open Oxygen Learning Hub member login">',
        '<div class="pillar-card pillar-card--learn" aria-label="Oxygen Learning Hub">'
    )
    content = content.replace(
        '<span class="pillar-button">Member Login <span aria-hidden="true">-&gt;</span></span>\n                    </a>',
        '<a href="login.html" class="pillar-button" style="text-decoration:none;">Member Login <span aria-hidden="true">-&gt;</span></a>\n                    </div>'
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_nested_links('index.html')
fix_nested_links('diagnostic.html')
