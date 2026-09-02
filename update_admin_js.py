import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update openUserModal
old_open_fields = """        if (!isNew) {
            const u = allUsersData.find(x => x.email === mode);
            if (u) {
                document.getElementById('u-name').value = u.name || '';
                document.getElementById('u-title').value = u.title || '';
                document.getElementById('u-role').value = u.role || 'employee';
                document.getElementById('u-gender').value = u.gender || 'male';
                
                if (document.getElementById('u-leader-email')) {
                    const lEmail = u.leaderEmail || '';
                    document.getElementById('u-leader-email').value = lEmail;
                    if (lEmail) {
                        const leaderData = allUsersData.find(x => x.email === lEmail);
                        if (leaderData) {
                            document.getElementById('u-leader-selected-content').innerHTML = `
                                <img src="${getAvatar(leaderData)}" class="w-6 h-6 rounded-full object-cover border border-slate-200">
                                <span class="font-black text-brand-navy">${leaderData.name}</span>
                                <span class="text-[9px] text-brand-blue bg-brand-blue/10 px-1.5 py-0.5 rounded ml-1">${leaderData.role}</span>
                            `;
                        }
                    } else {
                        document.getElementById('u-leader-selected-content').innerHTML = 'None (Direct to Admin/Supervisor)';
                    }
                }
                
                document.getElementById('u-online-limit').value = u.onlineDaysLimit || 0;
                document.getElementById('u-suspended').checked = !!u.isSuspended;
                
                if (u.permissions) {
                    document.getElementById('perm-crm').checked = !!u.permissions.crm;
                    document.getElementById('u-crm-role').value = u.permissions.crmRole || 'agent';
                    document.getElementById('perm-payroll').checked = !!u.permissions.payroll;
                }
                
                if (u.photo) {
                    document.getElementById('user-photo-preview').src = u.photo;
                    document.getElementById('user-photo-b64').value = u.photo;
                }
            }"""

new_open_fields = """        if (!isNew) {
            const u = allUsersData.find(x => x.email === mode);
            if (u) {
                document.getElementById('u-name').value = u.name || '';
                document.getElementById('u-title').value = u.title || '';
                document.getElementById('u-role').value = u.role || 'employee';
                document.getElementById('u-gender').value = u.gender || 'male';
                
                if (document.getElementById('u-leader-email')) {
                    const lEmail = u.leaderEmail || '';
                    document.getElementById('u-leader-email').value = lEmail;
                    if (lEmail) {
                        const leaderData = allUsersData.find(x => x.email === lEmail);
                        if (leaderData) {
                            document.getElementById('u-leader-selected-content').innerHTML = `
                                <img src="${getAvatar(leaderData)}" class="w-6 h-6 rounded-full object-cover border border-slate-200">
                                <span class="font-black text-brand-navy">${leaderData.name}</span>
                                <span class="text-[9px] text-brand-blue bg-brand-blue/10 px-1.5 py-0.5 rounded ml-1">${leaderData.role}</span>
                            `;
                        }
                    } else {
                        document.getElementById('u-leader-selected-content').innerHTML = 'None (Direct to Admin/Supervisor)';
                    }
                }
                
                document.getElementById('u-online-limit').value = u.onlineDaysLimit || 0;
                document.getElementById('u-suspended').checked = !!u.isSuspended;
                
                // Payroll fields
                document.getElementById('u-base-salary').value = u.baseSalary || '';
                document.getElementById('u-regularity-bonus').value = u.regularityBonus || '';
                document.getElementById('u-fixed-deductions').value = u.fixedDeductions || '';
                document.getElementById('u-allowance-val').value = (u.allowance && u.allowance.value) || '';
                document.getElementById('u-allowance-type').value = (u.allowance && u.allowance.type) || 'fixed';

                if (u.permissions) {
                    document.getElementById('perm-crm').checked = !!u.permissions.crm;
                    document.getElementById('u-crm-role').value = u.permissions.crmRole || 'agent';
                    document.getElementById('perm-payroll').checked = !!u.permissions.payroll;
                }
                
                if (u.photo) {
                    document.getElementById('user-photo-preview').src = u.photo;
                    document.getElementById('user-photo-b64').value = u.photo;
                }
            }"""

if old_open_fields in content:
    content = content.replace(old_open_fields, new_open_fields)
else:
    print("Warning: old_open_fields not found.")

# 2. Update saveUserData
old_save_fields = """        const data = {
            name: document.getElementById('u-name').value.trim(),
            title: document.getElementById('u-title').value.trim(),
            role: document.getElementById('u-role').value,
            gender: document.getElementById('u-gender').value,
            leaderEmail: document.getElementById('u-leader-email') ? document.getElementById('u-leader-email').value : '',
            onlineDaysLimit: onLimit,
            isSuspended: document.getElementById('u-suspended').checked,
            permissions: { 
                crm: document.getElementById('perm-crm').checked, 
                crmRole: document.getElementById('u-crm-role').value,
                payroll: document.getElementById('perm-payroll').checked 
            },
            photo: document.getElementById('user-photo-b64').value || ''
        };"""

new_save_fields = """        const data = {
            name: document.getElementById('u-name').value.trim(),
            title: document.getElementById('u-title').value.trim(),
            role: document.getElementById('u-role').value,
            gender: document.getElementById('u-gender').value,
            leaderEmail: document.getElementById('u-leader-email') ? document.getElementById('u-leader-email').value : '',
            onlineDaysLimit: onLimit,
            baseSalary: parseFloat(document.getElementById('u-base-salary').value) || 0,
            regularityBonus: parseFloat(document.getElementById('u-regularity-bonus').value) || 0,
            fixedDeductions: parseFloat(document.getElementById('u-fixed-deductions').value) || 0,
            allowance: {
                value: parseFloat(document.getElementById('u-allowance-val').value) || 0,
                type: document.getElementById('u-allowance-type').value
            },
            isSuspended: document.getElementById('u-suspended').checked,
            permissions: { 
                crm: document.getElementById('perm-crm').checked, 
                crmRole: document.getElementById('u-crm-role').value,
                payroll: document.getElementById('perm-payroll').checked 
            },
            photo: document.getElementById('user-photo-b64').value || ''
        };"""

if old_save_fields in content:
    content = content.replace(old_save_fields, new_save_fields)
else:
    print("Warning: old_save_fields not found.")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fields updated in JS functions.")
