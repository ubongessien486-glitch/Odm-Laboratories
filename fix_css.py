import re

def update_css_and_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update .pillar-card CSS to add position: relative;
    # Find .pillar-card {
    content = content.replace(
        '.pillar-card {\n            min-height: 520px;',
        '.pillar-card {\n            position: relative;\n            min-height: 520px;'
    )

    # 2. Add pseudo element to .pillar-button
    # Find .pillar-button {
    new_button_css = """        .pillar-button {
            position: relative;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            width: 100%;
            max-width: 100%;
            min-height: 54px;
            margin-top: auto;
            padding: 14px 22px;
            border-radius: 8px;
            color: var(--white);
            font-size: 15px;
            font-weight: 800;
            transition: background .2s ease, transform .2s ease, box-shadow .2s ease;
        }
        .pillar-button::after {
            content: '';
            position: absolute;
            top: 0; right: 0; bottom: 0; left: 0;
            /* Note: this expands to the nearest relatively positioned parent, which is the pillar-card */
        }
        .pillar-card { /* Ensure this targets the card for pseudo element bounds */ }
"""
    # Wait, the pseudo element needs its anchor. If .pillar-button has position: relative, the pseudo-element will only cover the button!
    # I should NOT give .pillar-button position: relative. 
    pass
