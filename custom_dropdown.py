import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace HTML
old_html = '''<div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Assigned Leader</label>
                        <select id="u-leader-email" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-3 text-sm font-bold outline-none focus:border-brand-blue cursor-pointer shadow-sm">
                            <option value="">None (Direct to Admin/Supervisor)</option>
                        </select></div>'''

new_html = '''<div class="relative"><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Assigned Leader</label>
                        <input type="hidden" id="u-leader-email" value="">
                        <div id="u-leader-select-btn" onclick="toggleLeaderDropdown()" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-3 flex items-center justify-between text-sm font-bold outline-none focus-within:border-brand-blue cursor-pointer shadow-sm">
                            <div id="u-leader-selected-content" class="flex items-center gap-2 text-slate-500 text-xs truncate">
                                None (Direct to Admin/Supervisor)
                            </div>
                            <i class="fas fa-chevron-down text-slate-400 text-xs"></i>
                        </div>
                        <div id="u-leader-dropdown" class="absolute z-50 w-full bg-white border border-slate-200 rounded-xl shadow-lg mt-1 hidden max-h-48 overflow-y-auto custom-scrollbar">
                            <!-- options injected via JS -->
                        </div>
                    </div>'''

content = content.replace(old_html, new_html)

# Replace JS in openUserModal
old_js = '''const leaderSelect = document.getElementById('u-leader-email');
        if (leaderSelect) {
            leaderSelect.innerHTML = '<option value="">None (Direct to Admin/Supervisor)</option>' +
                allUsersData.filter(x => x.role === 'leader' || x.role === 'supervisor').map(x => 
                    `<option value="${x.email}">${x.name} (${x.role === 'leader' ? 'Leader' : 'Supervisor'})</option>`
                ).join('');
        }'''

new_js = '''const leaderDropdown = document.getElementById('u-leader-dropdown');
        if (leaderDropdown) {
            const leaders = allUsersData.filter(x => x.role === 'leader' || x.role === 'supervisor');
            let dropdownHtml = `<div class="flex items-center gap-3 p-3 hover:bg-slate-50 cursor-pointer border-b border-slate-100 transition-colors" onclick="selectLeader('', 'None (Direct to Admin/Supervisor)', '')">
                                    <div class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-400 border border-slate-200 shrink-0"><i class="fas fa-user-slash text-xs"></i></div>
                                    <span class="text-xs font-bold text-slate-600">None (Direct to Admin/Supervisor)</span>
                                </div>`;
                                
            dropdownHtml += leaders.map(x => `
                <div class="flex items-center gap-3 p-3 hover:bg-slate-50 cursor-pointer border-b border-slate-100 transition-colors" onclick="selectLeader('${x.email}', '${x.name.replace(/'/g, "\\'")}', '${getAvatar(x)}')">
                    <img src="${getAvatar(x)}" class="w-8 h-8 rounded-full object-cover border border-slate-200 shadow-sm shrink-0">
                    <div class="flex flex-col truncate">
                        <span class="text-xs font-black text-brand-navy truncate">${x.name}</span>
                        <span class="text-[9px] font-bold text-textMuted uppercase">${x.role === 'leader' ? 'Leader' : 'Supervisor'}</span>
                    </div>
                </div>
            `).join('');
            
            leaderDropdown.innerHTML = dropdownHtml;
            
            const u = allUsersData.find(u => u.email === mode);
            const initialLeader = isNew ? '' : (u ? (u.leaderEmail || '') : '');
            
            if (!initialLeader) {
                selectLeader('', 'None (Direct to Admin/Supervisor)', '');
            } else {
                const lead = leaders.find(x => x.email === initialLeader);
                if (lead) {
                    selectLeader(lead.email, lead.name, getAvatar(lead));
                } else {
                    selectLeader('', 'None (Direct to Admin/Supervisor)', '');
                }
            }
        }'''

content = content.replace(old_js, new_js)

# Add global functions
global_funcs = '''
    window.toggleLeaderDropdown = function() {
        document.getElementById('u-leader-dropdown').classList.toggle('hidden');
    };
    
    window.selectLeader = function(email, name, avatarUrl) {
        document.getElementById('u-leader-email').value = email;
        const btn = document.getElementById('u-leader-selected-content');
        if (!email) {
            btn.innerHTML = `<span class="text-slate-500 text-xs">None (Direct to Admin/Supervisor)</span>`;
        } else {
            btn.innerHTML = `<img src="${avatarUrl}" class="w-6 h-6 rounded-full object-cover border border-slate-200 shadow-sm shrink-0"> <span class="text-brand-navy text-xs font-black truncate">${name}</span>`;
        }
        document.getElementById('u-leader-dropdown').classList.add('hidden');
    };
    
    document.addEventListener('click', function(e) {
        const dd = document.getElementById('u-leader-dropdown');
        const btn = document.getElementById('u-leader-select-btn');
        if (dd && !dd.classList.contains('hidden') && !dd.contains(e.target) && !btn.contains(e.target)) {
            dd.classList.add('hidden');
        }
    });

'''
content = content.replace('// INIT', global_funcs + '\n    // INIT')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("admin.html dropdown replaced successfully!")
