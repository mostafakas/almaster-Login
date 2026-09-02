import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The exact text that was injected multiple times
# We will find where it starts and ends
pattern = re.compile(r'\s*window\.switchUserFormTab = function\(tabName\) \{[\s\S]*?\}, 500\);\s*\}\s*', re.MULTILINE)

# Extract ONE copy of it to keep (or we can just reuse it)
match = pattern.search(content)
if not match:
    print("Could not find the injected script block to remove.")
    exit()

injected_text = match.group(0)

# Replace all occurrences with empty string
content = pattern.sub('', content)

# Now find the last </script> tag and inject it right before it
parts = content.rsplit('</script>', 1)
if len(parts) == 2:
    # Just in case `origRenderMonitorGrid` was still lying around somewhere
    injected_text_fixed = injected_text.replace("const origRenderMonitorGrid", "if(typeof origRenderMonitorGrid === 'undefined') { window.origRenderMonitorGrid = renderMonitorGrid; } else { window.origRenderMonitorGrid = origRenderMonitorGrid; }\n    renderMonitorGrid")
    
    content = parts[0] + injected_text_fixed + "\n</script>" + parts[1]

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Admin scripts fixed successfully.")
