import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract old form content from <form id="user-setup-form" ... to </form>
match = re.search(r'(<form id="user-setup-form"[\s\S]*?</form>)', content)
if not match:
    print("Could not find user-setup-form")
    exit(1)

old_form = match.group(1)

new_form = """<form id="user-setup-form" onsubmit="saveUserData(event)" class="flex-1 overflow-y-auto custom-scrollbar pr-2 flex flex-col">
                <input type="hidden" id="edit-mode-email">
                
                <!-- Tab Headers -->
                <div class="flex items-center gap-2 border-b border-slate-200 pb-2 mb-5 shrink-0 sticky top-0 bg-white z-10 pt-2">
                    <button type="button" onclick="switchUserFormTab('general')" id="tab-btn-general" class="px-4 py-2 text-xs font-black rounded-xl bg-brand-soft text-brand-blue transition-colors">General Info</button>
                    <button type="button" onclick="switchUserFormTab('hr')" id="tab-btn-hr" class="px-4 py-2 text-xs font-black text-slate-500 hover:bg-slate-100 rounded-xl transition-colors">HR & Payroll</button>
                    <button type="button" onclick="switchUserFormTab('kpi')" id="tab-btn-kpi" class="px-4 py-2 text-xs font-black text-slate-500 hover:bg-slate-100 rounded-xl transition-colors">KPIs & Evaluations</button>
                </div>
                
                <div class="flex-1 space-y-5 pb-5">
                    <!-- Tab Content: General -->
                    <div id="tab-content-general" class="space-y-5">
                        <div class="flex flex-col sm:flex-row gap-6 p-5 bg-surface border border-slate-200 rounded-2xl items-start sm:items-center">
                            <div class="relative cursor-pointer group shrink-0" onclick="document.getElementById('user-photo-upload').click()">
                                <img id="user-photo-preview" src="" class="w-24 h-24 rounded-full object-cover border-4 border-white shadow-md group-hover:border-brand-blueLt bg-white transition-all" alt="Avatar">
                                <div class="absolute inset-0 bg-black/40 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"><i class="fas fa-camera text-white"></i></div>
                                <input type="file" id="user-photo-upload" class="hidden" accept="image/*" onchange="previewUserPhoto(this)">
                                <input type="hidden" id="user-photo-b64">
                            </div>
                            <div class="flex-1 w-full grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Full Name</label><input type="text" id="u-name" required class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm"></div>
                                <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Job Title</label><input type="text" id="u-title" required class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm"></div>
                            </div>
                        </div>
                        
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Email Address</label><input type="email" id="u-email" required class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none disabled:bg-slate-50 disabled:text-slate-400 focus:border-brand-blue shadow-sm"></div>
                            <div id="password-container"><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Initial Password</label><input type="text" id="u-password" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none font-mono focus:border-brand-blue shadow-sm" placeholder="Min 6 chars"></div>
                        </div>
                        
                        <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
                            <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Role</label>
                                <select id="u-role" onchange="toggleLeaderSection()" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-3 text-sm font-bold outline-none focus:border-brand-blue cursor-pointer shadow-sm">
                                    <option value="employee">Employee</option><option value="leader">Leader</option><option value="supervisor">Supervisor</option><option value="admin">Admin</option>
                                </select></div>
                            <div class="relative"><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Assigned Leader</label>
                                <input type="hidden" id="u-leader-email" value="">
                                <div id="u-leader-select-btn" onclick="toggleLeaderDropdown()" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-3 flex items-center justify-between text-sm font-bold outline-none focus-within:border-brand-blue cursor-pointer shadow-sm">
                                    <div id="u-leader-selected-content" class="flex items-center gap-2 text-slate-500 text-xs truncate">
                                        None (Direct)
                                    </div>
                                    <i class="fas fa-chevron-down text-slate-400 text-xs"></i>
                                </div>
                                <div id="u-leader-dropdown" class="absolute z-[100] w-full bg-white border border-slate-200 rounded-2xl shadow-xl mt-2 hidden max-h-60 overflow-y-auto custom-scrollbar p-1.5 flex flex-col gap-1">
                                    <!-- options injected via JS -->
                                </div>
                            </div>
                            <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Gender</label>
                                <select id="u-gender" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-3 text-sm font-bold outline-none focus:border-brand-blue cursor-pointer shadow-sm" onchange="updateFallbackPreview()">
                                    <option value="male">Male</option><option value="female">Female</option>
                                </select></div>
                        </div>
                        
                        <div class="p-5 border border-slate-200 bg-surface rounded-2xl">
                            <p class="text-[10px] font-black text-textMain uppercase mb-3 tracking-widest border-b border-slate-200 pb-2"><i class="fas fa-shield-halved text-brand-blue mr-1"></i> Permissions & Access</p>
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm font-bold items-center">
                                <label class="flex items-center gap-3 cursor-pointer bg-white p-3 border border-slate-200 rounded-xl shadow-sm hover:border-brand-blueLt transition-colors"><input type="checkbox" id="perm-crm" class="w-4 h-4 rounded text-brand-blue focus:ring-brand-blue"> CRM System Access</label>
                                <div>
                                    <select id="u-crm-role" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-3 text-sm font-bold outline-none focus:border-brand-blue cursor-pointer shadow-sm">
                                        <option value="agent">CRM Role: Agent</option>
                                        <option value="supervisor">CRM Role: Supervisor</option>
                                        <option value="admin">CRM Role: Admin</option>
                                    </select>
                                </div>
                                <label class="flex items-center gap-3 cursor-pointer bg-white p-3 border border-slate-200 rounded-xl shadow-sm hover:border-brand-blueLt transition-colors"><input type="checkbox" id="perm-payroll" class="w-4 h-4 rounded text-brand-blue focus:ring-brand-blue"> Payroll System Access</label>
                            </div>
                        </div>

                        <div id="leader-team-section" class="p-5 border border-slate-200 bg-surface rounded-2xl hidden">
                            <p class="text-[10px] font-black text-textMain uppercase mb-3 tracking-widest border-b border-slate-200 pb-2"><i class="fas fa-users-viewfinder text-brand-blue mr-1"></i> Assigned Team Members (For This Leader)</p>
                            <div id="leader-team-list" class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 max-h-48 overflow-y-auto custom-scrollbar text-xs font-bold">
                                <!-- Checkboxes populated dynamically -->
                            </div>
                        </div>
                        
                        <div class="flex items-center justify-between p-5 bg-red-50 border border-red-200 rounded-2xl">
                            <div><span class="text-sm font-black text-red-700 block"><i class="fas fa-ban mr-1"></i> Suspend Account</span><span class="text-[10px] text-red-500/80 font-bold">Immediately block user from logging in.</span></div>
                            <label class="relative inline-flex items-center cursor-pointer"><input type="checkbox" id="u-suspended" class="sr-only peer"><div class="w-11 h-6 bg-slate-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-red-500"></div></label>
                        </div>
                    </div>

                    <!-- Tab Content: HR & Payroll -->
                    <div id="tab-content-hr" class="hidden space-y-5">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Vacation (Days)</label>
                                <input type="number" id="u-leave-balance" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="21"></div>
                            <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Online Limit (Days)</label>
                                <input type="number" id="u-online-limit" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="0"></div>
                        </div>
                        
                        <div class="p-5 border border-slate-200 bg-surface rounded-2xl space-y-4">
                            <p class="text-[10px] font-black text-textMain uppercase mb-3 tracking-widest border-b border-slate-200 pb-2"><i class="fas fa-money-bill-wave text-brand-blue mr-1"></i> Salary & Compensation</p>
                            <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Base Salary</label>
                                <input type="number" id="u-base-salary" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="e.g. 5000"></div>
                            
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Regularity Bonus (جزء الانتظام)</label>
                                    <input type="number" id="u-regularity-bonus" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="e.g. 500"></div>
                                <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Fixed Deductions (خصومات ثابتة)</label>
                                    <input type="number" id="u-fixed-deductions" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="e.g. 0"></div>
                            </div>
                        </div>

                        <div class="p-5 border border-slate-200 bg-surface rounded-2xl space-y-4">
                            <p class="text-[10px] font-black text-textMain uppercase mb-3 tracking-widest border-b border-slate-200 pb-2"><i class="fas fa-gift text-brand-blue mr-1"></i> Allowances (البدلات)</p>
                            <div class="grid grid-cols-3 gap-4 items-end">
                                <div class="col-span-2"><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Allowance Amount / Percentage</label>
                                    <input type="number" id="u-allowance-val" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="Amount"></div>
                                <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Type</label>
                                    <select id="u-allowance-type" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-3 text-sm font-bold outline-none focus:border-brand-blue cursor-pointer shadow-sm">
                                        <option value="fixed">Fixed ($)</option>
                                        <option value="percentage">Percentage (%)</option>
                                    </select></div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tab Content: KPIs -->
                    <div id="tab-content-kpi" class="hidden space-y-5">
                        <div class="p-5 border border-slate-200 bg-surface rounded-2xl flex flex-col items-center justify-center text-center py-12">
                            <i class="fas fa-chart-line text-4xl text-slate-200 mb-3"></i>
                            <h4 class="text-sm font-black text-textMain">KPI System Coming Soon</h4>
                            <p class="text-xs text-textMuted mt-1">You will be able to manage and view employee performance metrics here.</p>
                        </div>
                    </div>
                </div>

                <div class="pt-4 flex gap-3 border-t border-slate-100 shrink-0 sticky bottom-0 bg-white pb-2 z-10">
                    <button type="submit" id="save-user-btn" class="flex-1 py-3.5 bg-brand-blue text-white rounded-xl font-black text-sm shadow-lg hover:bg-brand-navy2 mini-btn"><i class="fas fa-save mr-2"></i> Save Employee</button>
                    <button type="button" id="delete-user-btn" onclick="deleteUser()" class="px-6 py-3.5 border border-red-200 bg-white text-red-500 hover:bg-red-50 rounded-xl font-black text-sm hidden transition-colors"><i class="fas fa-trash-alt mr-1"></i> Delete</button>
                </div>
            </form>"""

content = content.replace(old_form, new_form)

# Add the switchUserFormTab JS function near the end of the script tag
js_func = """
    window.switchUserFormTab = function(tabName) {
        ['general', 'hr', 'kpi'].forEach(t => {
            const btn = document.getElementById('tab-btn-' + t);
            const content = document.getElementById('tab-content-' + t);
            if (t === tabName) {
                btn.className = "px-4 py-2 text-xs font-black rounded-xl bg-brand-soft text-brand-blue transition-colors";
                content.classList.remove('hidden');
            } else {
                btn.className = "px-4 py-2 text-xs font-black text-slate-500 hover:bg-slate-100 rounded-xl transition-colors";
                content.classList.add('hidden');
            }
        });
    };
"""
if "window.switchUserFormTab" not in content:
    content = content.replace("</script>", js_func + "\n</script>")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Admin modal tabs implemented successfully.")
