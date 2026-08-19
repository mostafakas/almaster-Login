import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make the dropdown container look better (add p-1 for spacing, slightly increase max height)
old_dropdown_container = '''<div id="u-leader-dropdown" class="absolute z-50 w-full bg-white border border-slate-200 rounded-xl shadow-lg mt-1 hidden max-h-48 overflow-y-auto custom-scrollbar">'''
new_dropdown_container = '''<div id="u-leader-dropdown" class="absolute z-[100] w-full bg-white border border-slate-200 rounded-2xl shadow-xl mt-2 hidden max-h-60 overflow-y-auto custom-scrollbar p-1.5 flex flex-col gap-1">'''

content = content.replace(old_dropdown_container, new_dropdown_container)

# Change the JS generation part for dropdown items
old_js = '''const leaders = allUsersData.filter(x => x.role === 'leader' || x.role === 'supervisor');
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
            `).join('');'''

new_js = '''// Sort leaders: leaders first, then supervisors, then employees
            const leaders = [...allUsersData].sort((a,b) => {
                const w = {admin:1, supervisor:2, leader:3, employee:4};
                return (w[a.role]||5) - (w[b.role]||5);
            });
            let dropdownHtml = `<div class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-slate-50 cursor-pointer transition-all border border-transparent hover:border-slate-100 hover:shadow-sm" onclick="selectLeader('', 'None (Direct to Admin/Supervisor)', '')">
                                    <div class="w-9 h-9 rounded-full bg-slate-100 flex items-center justify-center text-slate-400 border border-slate-200 shrink-0"><i class="fas fa-user-slash text-xs"></i></div>
                                    <div class="flex flex-col">
                                        <span class="text-xs font-black text-slate-600">No Leader</span>
                                        <span class="text-[9px] font-bold text-slate-400">Direct to Admin/Supervisor</span>
                                    </div>
                                </div>`;
                                
            dropdownHtml += leaders.map(x => `
                <div class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-brand-soft cursor-pointer transition-all border border-transparent hover:border-brand-blue/20 hover:shadow-sm group" onclick="selectLeader('${x.email}', '${x.name.replace(/'/g, "\\'")}', '${getAvatar(x)}')">
                    <img src="${getAvatar(x)}" class="w-9 h-9 rounded-full object-cover border border-slate-200 shadow-sm shrink-0 group-hover:border-brand-blue/30 transition-colors">
                    <div class="flex flex-col truncate flex-1">
                        <span class="text-xs font-black text-brand-navy truncate group-hover:text-brand-blue transition-colors">${x.name}</span>
                        <div class="flex items-center gap-1 mt-0.5">
                            <span class="text-[8px] font-black px-1.5 py-0.5 rounded-md uppercase ${x.role === 'leader' ? 'bg-amber-100 text-amber-700' : (x.role === 'supervisor' ? 'bg-purple-100 text-purple-700' : 'bg-slate-100 text-slate-500')}">${x.role}</span>
                        </div>
                    </div>
                </div>
            `).join('');'''

content = content.replace(old_js, new_js)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated admin dropdown styling!")
