import os

required = [
    'Professional Summary', 'Career Objective', 'Technical Skills',
    'OfferLutBox', 'E-commerce', 'School Management',
    'Laravel', 'PHP', 'JavaScript', 'HTML', 'CSS', 'MySQL', 'AJAX',
    'REST API', 'Git', 'Flutter', 'SEO', 'Docker', 'Linux', 'VPS',
    'nobinmorsalin7@gmail.com', '+8801795456495',
    'Nasir Sikder', 'Ferdousi Begum',
    'Purbakandi, Damudya, Shariatpur', 'Figma', 'React', 'Next.js',
    'Design Philosophy', 'UI/UX', 'Responsive Design'
]

print("=" * 70)
print("CV CONTENT VERIFICATION")
print("=" * 70)

for filename in ['Nobin_Morsalin_ATS_Resume.pdf', 'Nobin_Morsalin_Designer_Resume.pdf']:
    if not os.path.exists(filename):
        print(f'\n✗ {filename}: FILE NOT FOUND')
        continue
        
    with open(filename, 'rb') as f:
        content_bytes = f.read()
    content = content_bytes.decode('latin1', errors='ignore')
    
    found = sum(1 for term in required if term.lower() in content.lower())
    missing = [term for term in required if term.lower() not in content.lower()]
    
    print(f'\n{filename}:')
    print(f'  ✓ Size: {len(content_bytes):,} bytes')
    print(f'  ✓ Content completeness: {found}/{len(required)} sections ({int(100*found/len(required))}%)')
    
    if missing:
        print(f'  ⚠ Missing sections: {missing}')
    else:
        print(f'  ✅ ALL REQUIRED CONTENT VERIFIED')
    
    # Show page count from PDF structure
    if b'/Count' in content_bytes:
        import re
        matches = re.findall(b'/Count (\d+)', content_bytes)
        if matches:
            page_count = int(matches[-1])
            print(f'  ✓ PDF Pages: {page_count}')

print("\n" + "=" * 70)
print("✅ CV Verification Complete")
print("=" * 70)
