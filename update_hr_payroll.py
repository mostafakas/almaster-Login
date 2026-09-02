import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HTML fields in tab-content-hr
old_hr_html = """                        <div class="p-5 border border-slate-200 bg-surface rounded-2xl space-y-4">
                            <p class="text-[10px] font-black text-textMain uppercase mb-3 tracking-widest border-b border-slate-200 pb-2"><i class="fas fa-money-bill-wave text-brand-blue mr-1"></i> Salary & Compensation</p>
                            <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Base Salary</label>
                                <input type="number" id="u-base-salary" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="e.g. 5000"></div>
                            
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Regularity Bonus (??? ????????)</label>
                                    <input type="number" id="u-regularity-bonus" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="e.g. 500"></div>
                                <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Fixed Deductions (?????? ?????)</label>
                                    <input type="number" id="u-fixed-deductions" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="e.g. 0"></div>
                            </div>
                        </div>

                        <div class="p-5 border border-slate-200 bg-surface rounded-2xl space-y-4">
                            <p class="text-[10px] font-black text-textMain uppercase mb-3 tracking-widest border-b border-slate-200 pb-2"><i class="fas fa-gift text-brand-blue mr-1"></i> Allowances (???????)</p>
                            <div class="grid grid-cols-3 gap-4 items-end">
                                <div class="col-span-2"><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Allowance Amount / Percentage</label>
                                    <input type="number" id="u-allowance-val" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="Amount"></div>
                                <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Type</label>
                                    <select id="u-allowance-type" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-3 text-sm font-bold outline-none focus:border-brand-blue cursor-pointer shadow-sm">
                                        <option value="fixed">Fixed ($)</option>
                                        <option value="percentage">Percentage (%)</option>
                                    </select></div>
                            </div>
                        </div>"""

new_hr_html = """                        <div class="p-5 border border-slate-200 bg-surface rounded-2xl space-y-4">
                            <p class="text-[10px] font-black text-textMain uppercase mb-3 tracking-widest border-b border-slate-200 pb-2"><i class="fas fa-money-bill-wave text-brand-blue mr-1"></i> Full Salary & Fixed Deductions</p>
                            
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Full Salary (الراتب الكامل)</label>
                                    <input type="number" id="u-full-salary" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="e.g. 10000"></div>
                                <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Fixed Deductions (خصومات ثابتة)</label>
                                    <input type="number" id="u-fixed-deductions" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="e.g. 0"></div>
                            </div>
                        </div>

                        <div class="p-5 border border-slate-200 bg-surface rounded-2xl space-y-4">
                            <p class="text-[10px] font-black text-textMain uppercase mb-3 tracking-widest border-b border-slate-200 pb-2"><i class="fas fa-gift text-brand-blue mr-1"></i> Compensation Breakdowns (البدلات والحوافز)</p>
                            
                            <!-- Allowances -->
                            <div class="grid grid-cols-3 gap-4 items-end mb-2">
                                <div class="col-span-2"><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Allowances (البدلات)</label>
                                    <input type="number" id="u-allowance-val" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="Amount"></div>
                                <div><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Type</label>
                                    <select id="u-allowance-type" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-3 text-sm font-bold outline-none focus:border-brand-blue cursor-pointer shadow-sm">
                                        <option value="fixed">Fixed ($)</option>
                                        <option value="percentage">Percentage (%)</option>
                                    </select></div>
                            </div>
                            
                            <!-- Incentives -->
                            <div class="grid grid-cols-3 gap-4 items-end mb-2">
                                <div class="col-span-2"><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">Incentives (الحوافز)</label>
                                    <input type="number" id="u-incentive-val" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="Amount"></div>
                                <div>
                                    <select id="u-incentive-type" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-3 text-sm font-bold outline-none focus:border-brand-blue cursor-pointer shadow-sm">
                                        <option value="fixed">Fixed ($)</option>
                                        <option value="percentage">Percentage (%)</option>
                                    </select></div>
                            </div>
                            
                            <!-- KPIs -->
                            <div class="grid grid-cols-3 gap-4 items-end">
                                <div class="col-span-2"><label class="text-[10px] font-black text-textMuted mb-1 block uppercase tracking-wider">KPIs Bonus (نسبة الكي بي آيز)</label>
                                    <input type="number" id="u-kpi-val" min="0" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm" placeholder="Amount"></div>
                                <div>
                                    <select id="u-kpi-type" class="w-full bg-white border border-slate-200 h-11 rounded-xl px-3 text-sm font-bold outline-none focus:border-brand-blue cursor-pointer shadow-sm">
                                        <option value="fixed">Fixed ($)</option>
                                        <option value="percentage">Percentage (%)</option>
                                    </select></div>
                            </div>
                        </div>"""
# Fix encoding issues in regex match for arabic chars
content = re.sub(r'<div class="p-5 border border-slate-200 bg-surface rounded-2xl space-y-4">\s*<p class="text-\[10px\] font-black text-textMain uppercase mb-3 tracking-widest border-b border-slate-200 pb-2"><i class="fas fa-money-bill-wave text-brand-blue mr-1"></i> Salary & Compensation</p>.*?<option value="percentage">Percentage \(%\)</option>\s*</select></div>\s*</div>\s*</div>', new_hr_html, content, flags=re.DOTALL)

# 2. Update openUserModal fields
old_open_fields = """            // Payroll fields
            document.getElementById('u-base-salary').value = u.baseSalary || '';
            document.getElementById('u-regularity-bonus').value = u.regularityBonus || '';
            document.getElementById('u-fixed-deductions').value = u.fixedDeductions || '';
            document.getElementById('u-allowance-val').value = (u.allowance && u.allowance.value) || '';
            document.getElementById('u-allowance-type').value = (u.allowance && u.allowance.type) || 'fixed';"""

new_open_fields = """            // Payroll fields
            document.getElementById('u-full-salary').value = u.fullSalary || '';
            document.getElementById('u-fixed-deductions').value = u.fixedDeductions || '';
            document.getElementById('u-allowance-val').value = (u.allowance && u.allowance.value) || '';
            document.getElementById('u-allowance-type').value = (u.allowance && u.allowance.type) || 'fixed';
            document.getElementById('u-incentive-val').value = (u.incentive && u.incentive.value) || '';
            document.getElementById('u-incentive-type').value = (u.incentive && u.incentive.type) || 'fixed';
            document.getElementById('u-kpi-val').value = (u.kpi && u.kpi.value) || '';
            document.getElementById('u-kpi-type').value = (u.kpi && u.kpi.type) || 'fixed';"""
content = content.replace(old_open_fields, new_open_fields)

# 3. Update saveUserData fields
old_save_fields = """            baseSalary: parseFloat(document.getElementById('u-base-salary').value) || 0,
            regularityBonus: parseFloat(document.getElementById('u-regularity-bonus').value) || 0,
            fixedDeductions: parseFloat(document.getElementById('u-fixed-deductions').value) || 0,
            allowance: {
                value: parseFloat(document.getElementById('u-allowance-val').value) || 0,
                type: document.getElementById('u-allowance-type').value
            },"""

new_save_fields = """            fullSalary: parseFloat(document.getElementById('u-full-salary').value) || 0,
            fixedDeductions: parseFloat(document.getElementById('u-fixed-deductions').value) || 0,
            allowance: {
                value: parseFloat(document.getElementById('u-allowance-val').value) || 0,
                type: document.getElementById('u-allowance-type').value
            },
            incentive: {
                value: parseFloat(document.getElementById('u-incentive-val').value) || 0,
                type: document.getElementById('u-incentive-type').value
            },
            kpi: {
                value: parseFloat(document.getElementById('u-kpi-val').value) || 0,
                type: document.getElementById('u-kpi-type').value
            },"""
content = content.replace(old_save_fields, new_save_fields)

# 4. Update generatePayslip function
old_payslip = """        const baseSalary = parseFloat(u.baseSalary) || 0;
        let allowance = 0;
        if (u.allowance && u.allowance.value) {
            if (u.allowance.type === 'percentage') {
                allowance = baseSalary * (parseFloat(u.allowance.value) / 100);
            } else {
                allowance = parseFloat(u.allowance.value);
            }
        }
        const regularityBonus = parseFloat(u.regularityBonus) || 0;
        const fixedDeductions = parseFloat(u.fixedDeductions) || 0;
        
        // Dynamic Delays / Deductions - Placeholder for future logic
        // We will add an input for the admin to manually input any delay deductions for this month
        
        const totalAdditions = baseSalary + allowance + regularityBonus;
        const totalDeductions = fixedDeductions;
        const netSalary = totalAdditions - totalDeductions;
        
        const html = `
            <div class="border-b border-slate-200 pb-6 mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div class="flex items-center gap-4">
                    <img src="${getAvatar(u)}" class="w-16 h-16 rounded-full border border-slate-200 object-cover shadow-sm">
                    <div>
                        <h3 class="text-xl font-black text-brand-navy">${u.name}</h3>
                        <p class="text-sm font-bold text-textMuted">${u.title || u.role} &bull; ${u.email}</p>
                    </div>
                </div>
                <div class="text-right">
                    <div class="text-xs font-black uppercase text-textMuted tracking-widest mb-1">Payslip For</div>
                    <div class="text-lg font-black text-brand-blue bg-brand-soft px-4 py-1.5 rounded-lg inline-block">${month}</div>
                </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                <!-- Additions -->
                <div>
                    <h4 class="text-xs font-black uppercase text-emerald-600 tracking-widest mb-4 flex items-center"><i class="fas fa-plus-circle mr-2"></i> Earnings</h4>
                    <div class="space-y-3">
                        <div class="flex justify-between items-center bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <span class="text-sm font-bold text-slate-600">Base Salary</span>
                            <span class="font-black text-brand-navy">${baseSalary.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between items-center bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <span class="text-sm font-bold text-slate-600">Allowances (${u.allowance?.type === 'percentage' ? u.allowance.value+'%' : 'Fixed'})</span>
                            <span class="font-black text-emerald-600">+ ${allowance.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between items-center bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <span class="text-sm font-bold text-slate-600">Regularity Bonus</span>
                            <span class="font-black text-emerald-600">+ ${regularityBonus.toFixed(2)}</span>
                        </div>
                    </div>
                    <div class="flex justify-between items-center mt-4 pt-4 border-t border-slate-200 px-3">
                        <span class="text-sm font-black text-brand-navy">Total Earnings</span>
                        <span class="font-black text-emerald-600 text-lg">${totalAdditions.toFixed(2)}</span>
                    </div>
                </div>"""

new_payslip = """        const fullSalary = parseFloat(u.fullSalary) || 0;
        
        let allowance = 0;
        if (u.allowance && u.allowance.value) {
            allowance = u.allowance.type === 'percentage' ? (fullSalary * (parseFloat(u.allowance.value) / 100)) : parseFloat(u.allowance.value);
        }
        
        let incentive = 0;
        if (u.incentive && u.incentive.value) {
            incentive = u.incentive.type === 'percentage' ? (fullSalary * (parseFloat(u.incentive.value) / 100)) : parseFloat(u.incentive.value);
        }
        
        let kpi = 0;
        if (u.kpi && u.kpi.value) {
            kpi = u.kpi.type === 'percentage' ? (fullSalary * (parseFloat(u.kpi.value) / 100)) : parseFloat(u.kpi.value);
        }
        
        const baseSalary = fullSalary - allowance - incentive - kpi;
        const fixedDeductions = parseFloat(u.fixedDeductions) || 0;
        
        // Dynamic Delays / Deductions - Placeholder for future logic
        // We will add an input for the admin to manually input any delay deductions for this month
        
        const totalAdditions = fullSalary; // The gross full salary
        const totalDeductions = fixedDeductions;
        const netSalary = totalAdditions - totalDeductions;
        
        const html = `
            <div class="border-b border-slate-200 pb-6 mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div class="flex items-center gap-4">
                    <img src="${getAvatar(u)}" class="w-16 h-16 rounded-full border border-slate-200 object-cover shadow-sm">
                    <div>
                        <h3 class="text-xl font-black text-brand-navy">${u.name}</h3>
                        <p class="text-sm font-bold text-textMuted">${u.title || u.role} &bull; ${u.email}</p>
                    </div>
                </div>
                <div class="text-right">
                    <div class="text-xs font-black uppercase text-textMuted tracking-widest mb-1">Payslip For</div>
                    <div class="text-lg font-black text-brand-blue bg-brand-soft px-4 py-1.5 rounded-lg inline-block">${month}</div>
                </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                <!-- Additions -->
                <div>
                    <h4 class="text-xs font-black uppercase text-emerald-600 tracking-widest mb-4 flex items-center"><i class="fas fa-plus-circle mr-2"></i> Earnings (From Full Salary)</h4>
                    <div class="space-y-3">
                        <div class="flex justify-between items-center bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <span class="text-sm font-bold text-slate-600">Basic Salary (Calculated)</span>
                            <span class="font-black text-brand-navy">${baseSalary.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between items-center bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <span class="text-sm font-bold text-slate-600">Allowances (${u.allowance?.type === 'percentage' ? u.allowance.value+'%' : 'Fixed'})</span>
                            <span class="font-black text-emerald-600">+ ${allowance.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between items-center bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <span class="text-sm font-bold text-slate-600">Incentives (${u.incentive?.type === 'percentage' ? u.incentive.value+'%' : 'Fixed'})</span>
                            <span class="font-black text-emerald-600">+ ${incentive.toFixed(2)}</span>
                        </div>
                        <div class="flex justify-between items-center bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <span class="text-sm font-bold text-slate-600">KPIs Bonus (${u.kpi?.type === 'percentage' ? u.kpi.value+'%' : 'Fixed'})</span>
                            <span class="font-black text-emerald-600">+ ${kpi.toFixed(2)}</span>
                        </div>
                    </div>
                    <div class="flex justify-between items-center mt-4 pt-4 border-t border-slate-200 px-3">
                        <span class="text-sm font-black text-brand-navy">Total Earnings (Full Salary)</span>
                        <span class="font-black text-emerald-600 text-lg">${totalAdditions.toFixed(2)}</span>
                    </div>
                </div>"""

# Replace payslip logic - use regex to match old_payslip to avoid exact match issues
content = content.replace(old_payslip, new_payslip)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HR fields and Payslip calculation")
