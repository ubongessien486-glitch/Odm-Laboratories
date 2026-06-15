import re

with open('employment-testing.html', 'r', encoding='utf-8') as f:
    emp_html = f.read()

match_precise = re.search(r'(<div class="product-body">.*?</div>\s*)<div class="product-sidebar">', emp_html, re.DOTALL)
if match_precise:
    content_to_inject = match_precise.group(1)
    
    with open('drug-free-workplace.html', 'r', encoding='utf-8') as f:
        dfw_html = f.read()
        
    injection = f'''
    <!-- EMPLOYMENT DRUG TESTING INFO CONTENT -->
    <section class="dfwp-section" style="padding-bottom: 0;">
        <div class="container product-layout">
            {content_to_inject}
        </div>
    </section>
    '''
    
    # Replace the section opening tag
    target = '<section class="dfwp-section dfwp-section--alt" id="pricing"'
    new_dfw_html = dfw_html.replace(target, injection + '\n    ' + target)
    
    with open('drug-free-workplace.html', 'w', encoding='utf-8') as f:
        f.write(new_dfw_html)
    print("Content injected successfully.")
else:
    print("Could not find product-body in employment-testing.html")
