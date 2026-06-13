import re

def fix_card_links(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to wrap the icon/kicker/h2 in an <a> tag pointing to the right place.
    # And we'll just leave the rest alone.
    
    # 1. Diagnostic Lab
    content = content.replace(
        '<div class="pillar-kicker">Clinical Services</div>\n                        <h2>Oxygen<br>Diagnostic Lab</h2>',
        '<a href="diagnostic.html" style="text-decoration:none; color:inherit; display:block;">\n                            <div class="pillar-kicker">Clinical Services</div>\n                            <h2>Oxygen<br>Diagnostic Lab</h2>\n                        </a>'
    )
    # The div already has cursor: pointer? No, we should add cursor pointer if we want the whole card. But we don't.
    # We will just let the title, the image, and the button be clickable.

    # 2. Home Care
    content = content.replace(
        '<img src="homecare-logo.svg" alt="Oxygen Home Care Agency Logo" style="height: 64px; width: auto; max-width: 100%; object-fit: contain; margin-bottom: 26px;" aria-hidden="true">\n                        <div class="pillar-kicker">HCSSA Licensed</div>\n                        <h2>Oxygen<br>Home Care Agency</h2>',
        '<a href="homecare.html" style="text-decoration:none; color:inherit; display:block;">\n                            <img src="homecare-logo.svg" alt="Oxygen Home Care Agency Logo" style="height: 64px; width: auto; max-width: 100%; object-fit: contain; margin-bottom: 26px;" aria-hidden="true">\n                            <div class="pillar-kicker">HCSSA Licensed</div>\n                            <h2>Oxygen<br>Home Care Agency</h2>\n                        </a>'
    )

    # 3. Learning Hub
    content = content.replace(
        '<img src="learning-hub-logo-new.png" alt="Oxygen Learning Hub Logo" style="height: 64px; width: auto; max-width: 100%; object-fit: contain; margin-bottom: 26px;" aria-hidden="true">\n                        <div class="pillar-kicker">Premium Member Access</div>\n                        <h2>Oxygen<br>Learning Hub</h2>',
        '<a href="login.html" style="text-decoration:none; color:inherit; display:block;">\n                            <img src="learning-hub-logo-new.png" alt="Oxygen Learning Hub Logo" style="height: 64px; width: auto; max-width: 100%; object-fit: contain; margin-bottom: 26px;" aria-hidden="true">\n                            <div class="pillar-kicker">Premium Member Access</div>\n                            <h2>Oxygen<br>Learning Hub</h2>\n                        </a>'
    )
    
    # Let's add cursor: pointer to the card itself and a window.location.href to make the whole card clickable for better UX
    content = content.replace(
        '<div class="pillar-card pillar-card--lab" aria-label="Oxygen Diagnostic Lab">',
        '<div class="pillar-card pillar-card--lab" aria-label="Oxygen Diagnostic Lab" style="cursor:pointer;" onclick="if(event.target.tagName.toLowerCase() !== \'a\') window.location.href=\'diagnostic.html\';">'
    )
    content = content.replace(
        '<div class="pillar-card pillar-card--home" aria-label="Oxygen Home Care Agency">',
        '<div class="pillar-card pillar-card--home" aria-label="Oxygen Home Care Agency" style="cursor:pointer;" onclick="if(event.target.tagName.toLowerCase() !== \'a\') window.location.href=\'homecare.html\';">'
    )
    content = content.replace(
        '<div class="pillar-card pillar-card--learn" aria-label="Oxygen Learning Hub">',
        '<div class="pillar-card pillar-card--learn" aria-label="Oxygen Learning Hub" style="cursor:pointer;" onclick="if(event.target.tagName.toLowerCase() !== \'a\') window.location.href=\'login.html\';">'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_card_links('index.html')
fix_card_links('diagnostic.html')
