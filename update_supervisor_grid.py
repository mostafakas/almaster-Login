import re

with open('supervisor.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update monitor-grid container to remove grid classes
old_grid = '<div id="monitor-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-3 content-start pb-10"></div>'
new_grid = '<div id="monitor-grid" class="w-full pb-10 flex flex-col gap-6"></div>'
content = content.replace(old_grid, new_grid)

# 2. Update listenToAllUsers to remove the filter
old_listen = "allUsersData = snap.docs.map(d => ({ email: d.id, ...d.data() })).filter(u => u.leaderEmail === currentUser.email);"
new_listen = "allUsersData = snap.docs.map(d => ({ email: d.id, ...d.data() }));"
content = content.replace(old_listen, new_listen)

# 3. Update renderMonitorGrid to render two sections
old_render = '''    function renderMonitorGrid() {
        const container = document.getElementById('monitor-grid'); if (!container) return;
        const term = (document.getElementById('monitor-search').value || '').toLowerCase().trim();
        
        let filtered = allUsersData.filter(u => {
            if (currentMonitorFilter !== 'all' && (u.status || 'Offline') !== currentMonitorFilter) return false;
            if (term && !(u.name || '').toLowerCase().includes(term) && !(u.email || '').toLowerCase().includes(term)) return false;
            return true;
        });
        
        if (filtered.length === 0) {
            container.innerHTML = `<div class="col-span-full py-10 flex flex-col items-center justify-center text-slate-400 w-full"><i class="fas fa-search text-3xl mb-3 opacity-50"></i><p class="text-xs font-bold">No employees found.</p></div>`;
            return;
        }

        container.innerHTML = filtered.map(generateUserCardHTML).join('');
    }'''

new_render = '''    function renderMonitorGrid() {
        const container = document.getElementById('monitor-grid'); if (!container) return;
        const term = (document.getElementById('monitor-search').value || '').toLowerCase().trim();
        
        let filtered = allUsersData.filter(u => {
            if (currentMonitorFilter !== 'all' && (u.status || 'Offline') !== currentMonitorFilter) return false;
            if (term && !(u.name || '').toLowerCase().includes(term) && !(u.email || '').toLowerCase().includes(term)) return false;
            return true;
        });
        
        if (filtered.length === 0) {
            container.innerHTML = `<div class="py-10 flex flex-col items-center justify-center text-slate-400 w-full"><i class="fas fa-search text-3xl mb-3 opacity-50"></i><p class="text-xs font-bold">No employees found.</p></div>`;
            return;
        }

        const leaders = filtered.filter(u => u.role === 'leader' || u.role === 'supervisor' || u.role === 'admin');
        const employees = filtered.filter(u => u.role !== 'leader' && u.role !== 'supervisor' && u.role !== 'admin');

        let html = '';
        
        const gridClasses = "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-3 content-start";

        if (leaders.length > 0) {
            html += `
                <div>
                    <h3 class="text-sm font-black text-brand-navy mb-3 px-1 border-b border-slate-200 pb-2"><i class="fas fa-crown text-amber-500 mr-2"></i> Leaders & Supervisors</h3>
                    <div class="${gridClasses}">
                        ${leaders.map(generateUserCardHTML).join('')}
                    </div>
                </div>
            `;
        }

        if (employees.length > 0) {
            html += `
                <div>
                    <h3 class="text-sm font-black text-brand-navy mb-3 px-1 border-b border-slate-200 pb-2"><i class="fas fa-users text-brand-blue mr-2"></i> Team Members</h3>
                    <div class="${gridClasses}">
                        ${employees.map(generateUserCardHTML).join('')}
                    </div>
                </div>
            `;
        }

        container.innerHTML = html;
    }'''

content = content.replace(old_render, new_render)

with open('supervisor.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated supervisor dashboard!")
