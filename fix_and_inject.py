import re

def fix_and_inject():
    filename = 'admin.html'
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Expand Payroll Tab
    content = content.replace('<div class="max-w-6xl mx-auto w-full space-y-6">', '<div class="w-full space-y-6">')

    # 2. Inject Daily Attendance Button
    nav_daily_attendance = """
            <button onclick="switchTab('daily-attendance')" id="nav-daily-attendance" class="nav-link text-textMuted w-full flex items-center gap-4 px-3 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue group/item">
                <i class="fas fa-calendar-check text-lg text-center w-6 shrink-0 group-hover/item:scale-110 transition-transform text-emerald-500"></i> 
                <span class="whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 delay-75">Daily Attendance</span>
            </button>
"""
    if 'id="nav-daily-attendance"' not in content:
        content = content.replace('id="nav-payroll"', nav_daily_attendance.strip() + '\n            <button onclick="switchTab(\'payroll\')" id="nav-payroll"')

    # 3. Inject Daily Attendance Tab Container
    tab_daily_attendance = """
        <!-- Daily Attendance Tab -->
        <div id="tab-daily-attendance" class="tab-pane hidden flex-col flex-1 h-full overflow-hidden">
            <div class="px-8 py-6 border-b border-slate-100 bg-white shrink-0 flex flex-wrap gap-4 items-center justify-between">
                <div>
                    <h2 class="text-xl font-black text-textMain tracking-tight">Daily Attendance</h2>
                    <p class="text-xs font-bold text-textMuted mt-1">Track presence, late arrivals, and manage leaves.</p>
                </div>
                <div class="flex items-center gap-3">
                    <input type="date" id="att-date-picker" class="border border-slate-200 rounded-xl px-4 py-2 text-sm font-bold text-textMain focus:ring-2 focus:ring-brand-blue focus:outline-none">
                    <button onclick="loadAttendance()" class="px-5 py-2.5 bg-brand-navy text-white text-xs font-black rounded-xl hover:bg-brand-blue transition-colors shadow-sm"><i class="fas fa-search me-2"></i> View Report</button>
                </div>
            </div>
            
            <div class="flex-1 p-8 overflow-y-auto custom-scrollbar">
                <div class="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden w-full">
                    <div class="overflow-x-auto w-full">
                        <table class="w-full text-left border-collapse min-w-full">
                            <thead>
                                <tr class="bg-slate-50 border-b border-slate-100 text-[10px] uppercase font-black text-slate-400 tracking-wider">
                                    <th class="px-6 py-4">Employee</th>
                                    <th class="px-6 py-4">Status</th>
                                    <th class="px-6 py-4">Time In</th>
                                    <th class="px-6 py-4">Time Out</th>
                                    <th class="px-6 py-4">Late?</th>
                                    <th class="px-6 py-4 text-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody id="attendance-tbody" class="text-sm font-bold divide-y divide-slate-50 text-textMain">
                                <!-- Populated by JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
"""
    if 'id="tab-daily-attendance"' not in content:
        content = content.replace('<div id="tab-payroll"', tab_daily_attendance + '\n        <div id="tab-payroll"')

    # Fix JS loadAttendance logic so it runs on switchTab if needed
    if "if(tabId === 'daily-attendance') loadAttendance();" not in content:
        content = content.replace("if(tabId === 'attendance') loadAttendance();", "if(tabId === 'daily-attendance') loadAttendance();")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Injected successfully!")

fix_and_inject()
