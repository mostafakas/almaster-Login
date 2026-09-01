import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_sidebar = """    <aside class="w-64 bg-white border-r border-slate-100 flex flex-col z-20 shadow-xl transition-all shrink-0">
        <!-- Logo Area -->
        <div class="h-20 flex items-center justify-center gap-3 px-6 border-b border-slate-50 shrink-0">
            <svg viewBox="0 0 24 24" class="w-7 h-7 text-brand-blueLt" fill="#2563eb" aria-hidden="true"><path d="M12 0l2.4 9.6L24 12l-9.6 2.4L12 24l-2.4-9.6L0 12l9.6-2.4z"/></svg>
            <h1 class="text-xl font-black tracking-tight">AL<span class="text-brand-blue"> MASTER</span></h1>
        </div>
        <!-- Nav Links -->
        <nav class="flex-1 p-4 space-y-2 overflow-y-auto custom-scrollbar">
            <button onclick="switchTab('dashboard')" id="nav-dashboard" class="nav-link active bg-brand-soft text-brand-blue w-full flex items-center gap-3 px-4 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue">
                <i class="fas fa-chart-pie w-5 text-center text-lg"></i> Dashboard
            </button>
            <button onclick="switchTab('hr')" id="nav-hr" class="nav-link text-textMuted w-full flex items-center gap-3 px-4 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue">
                <i class="fas fa-users-cog w-5 text-center text-lg"></i> HR & Employees
            </button>
            <button onclick="switchTab('requests')" id="nav-requests" class="nav-link text-textMuted w-full flex items-center justify-between px-4 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue">
                <div class="flex items-center gap-3"><i class="fas fa-envelope-open-text w-5 text-center text-lg"></i> Requests</div>
                <span id="nav-pending-badge" class="bg-red-500 text-white text-[10px] font-black px-2 py-0.5 rounded-full hidden shadow-sm">0</span>
            </button>
            <button onclick="switchTab('attendance')" id="nav-attendance" class="nav-link text-textMuted w-full flex items-center gap-3 px-4 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue">
                <i class="fas fa-user-clock w-5 text-center text-lg"></i> Attendance Control
            </button>
            <button onclick="window.open('sales_app.html', '_blank')" class="nav-link text-textMuted w-full flex items-center gap-3 px-4 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue border border-transparent hover:border-brand-blueLt mt-4 bg-slate-50">
                <i class="fas fa-briefcase w-5 text-center text-lg text-brand-blue"></i> Sales CRM
            </button>
        </nav>
        <!-- Sidebar Footer (Stats/Overview) -->
        <div class="p-4 border-t border-slate-100 bg-slate-50 shrink-0 text-center">
            <div class="text-[10px] font-black text-textMuted uppercase mb-2 tracking-widest">Active System</div>
            <div id="sidebar-counts" class="flex flex-wrap gap-1 justify-center"></div>
        </div>
    </aside>"""

new_sidebar = """    <aside class="w-[76px] hover:w-64 group bg-white border-r border-slate-100 flex flex-col z-50 shadow-xl transition-all duration-300 ease-out overflow-hidden shrink-0 absolute h-full sm:relative">
        <!-- Logo Area -->
        <div class="h-20 flex items-center gap-3 px-6 border-b border-slate-50 shrink-0 w-64">
            <svg viewBox="0 0 24 24" class="w-7 h-7 text-brand-blueLt shrink-0" fill="#2563eb" aria-hidden="true"><path d="M12 0l2.4 9.6L24 12l-9.6 2.4L12 24l-2.4-9.6L0 12l9.6-2.4z"/></svg>
            <h1 class="text-xl font-black tracking-tight whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 delay-75">AL<span class="text-brand-blue"> MASTER</span></h1>
        </div>
        <!-- Nav Links -->
        <nav class="flex-1 p-3 space-y-2 overflow-y-auto overflow-x-hidden custom-scrollbar">
            <button onclick="switchTab('dashboard')" id="nav-dashboard" class="nav-link active bg-brand-soft text-brand-blue w-full flex items-center gap-4 px-3 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue group/item">
                <i class="fas fa-chart-pie text-lg text-center w-6 shrink-0 group-hover/item:scale-110 transition-transform"></i> 
                <span class="whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 delay-75">Dashboard</span>
            </button>
            <button onclick="switchTab('hr')" id="nav-hr" class="nav-link text-textMuted w-full flex items-center gap-4 px-3 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue group/item">
                <i class="fas fa-users-cog text-lg text-center w-6 shrink-0 group-hover/item:scale-110 transition-transform"></i> 
                <span class="whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 delay-75">HR & Employees</span>
            </button>
            <button onclick="switchTab('requests')" id="nav-requests" class="nav-link text-textMuted w-full flex items-center gap-4 px-3 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue group/item relative">
                <i class="fas fa-envelope-open-text text-lg text-center w-6 shrink-0 group-hover/item:scale-110 transition-transform"></i> 
                <span class="whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 delay-75 flex-1 text-left">Requests</span>
                <span id="nav-pending-badge" class="absolute right-3 bg-red-500 text-white text-[10px] font-black px-2 py-0.5 rounded-full hidden shadow-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300">0</span>
            </button>
            <button onclick="switchTab('attendance')" id="nav-attendance" class="nav-link text-textMuted w-full flex items-center gap-4 px-3 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue group/item">
                <i class="fas fa-user-clock text-lg text-center w-6 shrink-0 group-hover/item:scale-110 transition-transform"></i> 
                <span class="whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 delay-75">Attendance Control</span>
            </button>
            
            <div class="h-px bg-slate-100 w-full my-2"></div>
            
            <button onclick="switchTab('payroll')" id="nav-payroll" class="nav-link text-textMuted w-full flex items-center gap-4 px-3 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue group/item">
                <i class="fas fa-file-invoice-dollar text-lg text-center w-6 shrink-0 group-hover/item:scale-110 transition-transform text-amber-500"></i> 
                <span class="whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 delay-75">Payroll & Payslip</span>
            </button>
            <button onclick="switchTab('reports')" id="nav-reports" class="nav-link text-textMuted w-full flex items-center gap-4 px-3 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue group/item">
                <i class="fas fa-chart-line text-lg text-center w-6 shrink-0 group-hover/item:scale-110 transition-transform text-emerald-500"></i> 
                <span class="whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 delay-75">Full Reports</span>
            </button>

            <button onclick="window.open('sales_app.html', '_blank')" class="nav-link text-textMuted w-full flex items-center gap-4 px-3 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue border border-transparent hover:border-brand-blueLt mt-4 bg-slate-50 group/item">
                <i class="fas fa-briefcase text-lg text-center w-6 shrink-0 group-hover/item:scale-110 transition-transform text-brand-blue"></i> 
                <span class="whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 delay-75">Sales CRM</span>
            </button>
        </nav>
        <!-- Sidebar Footer -->
        <div class="p-3 border-t border-slate-100 bg-slate-50 shrink-0 flex justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <div class="w-full">
                <div class="text-[9px] font-black text-textMuted uppercase mb-2 tracking-widest text-center whitespace-nowrap">Active System</div>
                <div id="sidebar-counts" class="flex flex-wrap gap-1 justify-center whitespace-nowrap"></div>
            </div>
        </div>
    </aside>"""

if old_sidebar in content:
    content = content.replace(old_sidebar, new_sidebar)
    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Sidebar updated successfully!")
else:
    print("Old sidebar not found.")
