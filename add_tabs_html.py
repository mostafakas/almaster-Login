import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_tabs = """
        <!-- Tab: Payroll & Payslip -->
        <div id="tab-payroll" class="tab-pane hidden flex-col flex-1 h-full relative overflow-y-auto custom-scrollbar p-4 md:p-8">
            <div class="max-w-6xl mx-auto w-full space-y-6">
                <!-- Header -->
                <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
                    <div>
                        <h2 class="text-2xl md:text-3xl font-black text-brand-navy tracking-tight mb-2">Payroll & <span class="text-brand-blue">Payslip</span></h2>
                        <p class="text-sm font-bold text-textMuted">Generate and manage employee salaries.</p>
                    </div>
                </div>
                
                <!-- Main Controls -->
                <div class="bg-white rounded-3xl p-6 shadow-sm border border-slate-100 flex flex-col md:flex-row gap-4 items-end">
                    <div class="flex-1 w-full">
                        <label class="text-[10px] font-black text-textMuted mb-2 block uppercase tracking-wider">Select Employee</label>
                        <select id="payroll-employee-select" class="w-full bg-slate-50 border border-slate-200 h-12 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm">
                            <option value="">-- Choose Employee --</option>
                        </select>
                    </div>
                    <div class="w-full md:w-48 shrink-0">
                        <label class="text-[10px] font-black text-textMuted mb-2 block uppercase tracking-wider">Month</label>
                        <input type="month" id="payroll-month" class="w-full bg-slate-50 border border-slate-200 h-12 rounded-xl px-4 text-sm font-bold outline-none focus:border-brand-blue shadow-sm">
                    </div>
                    <button onclick="generatePayslip()" class="h-12 px-8 bg-brand-blue text-white rounded-xl font-black text-sm shadow-lg hover:bg-brand-navy2 transition-colors shrink-0 w-full md:w-auto"><i class="fas fa-file-invoice-dollar mr-2"></i> Generate</button>
                </div>

                <!-- Payslip Result -->
                <div id="payslip-result" class="hidden bg-white rounded-3xl p-6 shadow-sm border border-slate-100 mt-6 relative">
                    <button onclick="printPayslip()" class="absolute top-6 right-6 px-4 py-2 bg-slate-100 text-slate-600 hover:bg-brand-blue hover:text-white rounded-lg text-xs font-black transition-colors"><i class="fas fa-print mr-2"></i> Print</button>
                    
                    <div id="payslip-content" class="pt-8 md:pt-4">
                        <!-- Injected via JS -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab: Reports -->
        <div id="tab-reports" class="tab-pane hidden flex-col flex-1 h-full relative overflow-y-auto custom-scrollbar p-4 md:p-8">
            <div class="max-w-6xl mx-auto w-full space-y-6">
                <!-- Header -->
                <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
                    <div>
                        <h2 class="text-2xl md:text-3xl font-black text-brand-navy tracking-tight mb-2">Comprehensive <span class="text-brand-blue">Reports</span></h2>
                        <p class="text-sm font-bold text-textMuted">View and export full HR analytics.</p>
                    </div>
                </div>
                
                <div class="bg-white rounded-3xl p-12 shadow-sm border border-slate-100 flex flex-col items-center justify-center text-center">
                    <i class="fas fa-tools text-5xl text-brand-blueLt mb-4"></i>
                    <h3 class="text-xl font-black text-brand-navy">Reports Module Coming Soon</h3>
                    <p class="text-sm text-textMuted mt-2 max-w-md">The comprehensive reporting engine is currently being built. It will allow you to export detailed monthly logs, performance metrics, and location tracking.</p>
                </div>
            </div>
        </div>
"""

# Insert before <!-- Logs Modal -->
content = content.replace("    <!-- Logs Modal -->", new_tabs + "\n    <!-- Logs Modal -->")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Payroll and Reports tabs added.")
