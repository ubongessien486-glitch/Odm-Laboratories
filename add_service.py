import re

service_0 = '''
                <!-- Service 0 (New Employment Testing) -->
                <div class="service-card" style="padding-top:0;">
                    <img loading="lazy" decoding="async" height="900" width="900" src="lady-doctor.webp" alt="Employment Drug Testing" style="width:100%; height:180px; object-fit:cover; border-radius:12px 12px 0 0; margin: 0 -28px 20px; width:calc(100% + 56px);">
                    <h3>EMPLOYMENT DRUG TESTING</h3>
                    <p>Structured drug-free workplace programs including pre-employment, random, and post-accident testing.</p>
                    <a href="employment-testing.html" class="service-link">View Details <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
                </div>
'''

for file in ['diagnostic.html', 'index.html']:
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Check if Service 0 is already there to avoid duplicates
    if 'Service 0 (New Employment Testing)' not in html:
        # Insert Service 0 right after <div class="services-grid" id="services-grid-live">
        html = re.sub(r'(<div class="services-grid"[^>]*>)', r'\1' + service_0, html)
        with open(file, 'w', encoding='utf-8') as out:
            out.write(html)
        print(f"Added Service 0 to {file}")

