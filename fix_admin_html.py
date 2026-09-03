import re

def fix_admin_html():
    with open('admin.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove the misplaced JS logic from the Tailwind script tag
    # The logic starts with "// --- Attendance Logic ---" and ends with "// --- End Attendance Logic ---"
    logic_pattern = r'(\s*// --- Attendance Logic ---.*?// --- End Attendance Logic ---\s*)'
    matches = re.findall(logic_pattern, content, flags=re.DOTALL)
    if matches:
        js_code = matches[0]
        # Remove it from wherever it is
        content = content.replace(js_code, '')
        
        # Inject it right before the LAST </script> tag
        # Find the last occurrence of </script>
        last_script_idx = content.rfind('</script>')
        if last_script_idx != -1:
            content = content[:last_script_idx] + js_code + '\n' + content[last_script_idx:]
            print("Moved JS logic to the correct main script block.")

    # 2. Fix the styling of tab-daily-attendance so it matches the other tabs
    # Current: class="tab-pane hidden flex-col flex-1 h-full overflow-hidden"
    # Target: class="tab-pane absolute inset-0 p-6 hidden flex-col gap-5"
    old_class = 'class="tab-pane hidden flex-col flex-1 h-full overflow-hidden"'
    new_class = 'class="tab-pane absolute inset-0 p-6 hidden flex-col gap-5"'
    if old_class in content:
        content = content.replace(old_class, new_class)
        print("Fixed daily-attendance tab styling.")

    # Let's also fix tab-payroll styling just in case it doesn't match
    # It was: class="tab-pane hidden flex-col flex-1 h-full relative overflow-y-auto custom-scrollbar p-4 md:p-8"
    # We can make it: class="tab-pane absolute inset-0 p-6 hidden flex-col gap-5 overflow-y-auto custom-scrollbar"
    old_payroll_class = 'class="tab-pane hidden flex-col flex-1 h-full relative overflow-y-auto custom-scrollbar p-4 md:p-8"'
    new_payroll_class = 'class="tab-pane absolute inset-0 p-6 hidden flex-col gap-5 overflow-y-auto custom-scrollbar"'
    if old_payroll_class in content:
        content = content.replace(old_payroll_class, new_payroll_class)
        print("Fixed payroll tab styling.")

    # Check if we accidentally created nested or messed up button classes earlier
    if '<button onclick="switchTab(\'payroll\')" <button' in content:
        content = content.replace('<button onclick="switchTab(\'payroll\')" <button', '<button')

    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(content)

fix_admin_html()
