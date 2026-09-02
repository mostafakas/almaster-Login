import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

js_payroll = """
    // --- PAYROLL SYSTEM ---
    function initPayrollDropdown() {
        const sel = document.getElementById('payroll-employee-select');
        if (!sel) return;
        const currentVal = sel.value;
        sel.innerHTML = '<option value="">-- Choose Employee --</option>';
        const sorted = [...allUsersData].sort((a,b) => (a.name||'').localeCompare(b.name||''));
        sorted.forEach(u => {
            const opt = document.createElement('option');
            opt.value = u.email;
            opt.textContent = `${u.name} (${u.role})`;
            sel.appendChild(opt);
        });
        if (currentVal && allUsersData.find(u => u.email === currentVal)) sel.value = currentVal;
        
        const mInput = document.getElementById('payroll-month');
        if (!mInput.value) {
            const d = new Date();
            mInput.value = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
        }
    }
    
    // Call initPayrollDropdown when users are loaded
    const origRenderMonitorGrid = renderMonitorGrid;
    renderMonitorGrid = function() {
        origRenderMonitorGrid();
        initPayrollDropdown();
    };

    window.generatePayslip = async function() {
        const email = document.getElementById('payroll-employee-select').value;
        const month = document.getElementById('payroll-month').value;
        
        if (!email || !month) {
            showToast('Error', 'Please select an employee and a month.', 'error');
            return;
        }
        
        const u = allUsersData.find(x => x.email === email);
        if (!u) return;
        
        const baseSalary = parseFloat(u.baseSalary) || 0;
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
                </div>
                
                <!-- Deductions -->
                <div>
                    <h4 class="text-xs font-black uppercase text-red-500 tracking-widest mb-4 flex items-center"><i class="fas fa-minus-circle mr-2"></i> Deductions</h4>
                    <div class="space-y-3">
                        <div class="flex justify-between items-center bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <span class="text-sm font-bold text-slate-600">Fixed Deductions</span>
                            <span class="font-black text-red-500">- ${fixedDeductions.toFixed(2)}</span>
                        </div>
                        
                        <div class="flex justify-between items-center bg-orange-50 p-3 rounded-lg border border-orange-100 border-dashed">
                            <span class="text-xs font-bold text-orange-600">Delay Deductions<br><span class="text-[9px] font-medium">(Awaiting future rules)</span></span>
                            <span class="font-black text-orange-600">0.00</span>
                        </div>
                    </div>
                    <div class="flex justify-between items-center mt-4 pt-4 border-t border-slate-200 px-3">
                        <span class="text-sm font-black text-brand-navy">Total Deductions</span>
                        <span class="font-black text-red-500 text-lg">${totalDeductions.toFixed(2)}</span>
                    </div>
                </div>
            </div>
            
            <div class="bg-brand-navy text-white rounded-2xl p-6 shadow-xl flex flex-col md:flex-row justify-between items-center gap-4">
                <div>
                    <span class="text-xs font-bold text-slate-400 uppercase tracking-widest block mb-1">Net Payable Salary</span>
                    <span class="text-3xl font-black">${netSalary.toFixed(2)} EGP</span>
                </div>
                <div class="w-full md:w-auto h-px md:h-12 w-12 md:w-px bg-white/20"></div>
                <div class="text-center md:text-right w-full md:w-auto">
                    <p class="text-xs font-bold text-slate-400">Generated On</p>
                    <p class="text-sm font-bold text-white">${new Date().toLocaleDateString('en-GB')}</p>
                </div>
            </div>
        `;
        
        document.getElementById('payslip-content').innerHTML = html;
        document.getElementById('payslip-result').classList.remove('hidden');
    }

    window.printPayslip = function() {
        const content = document.getElementById('payslip-content').innerHTML;
        const win = window.open('', '_blank');
        win.document.write(`
            <html>
                <head>
                    <title>Payslip</title>
                    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
                    <style> @media print { body { -webkit-print-color-adjust: exact; } } </style>
                </head>
                <body class="p-10 font-sans">
                    <h1 class="text-center font-black text-3xl mb-8 text-blue-600">AL MASTER - PAYSLIP</h1>
                    ${content}
                    <div class="mt-16 pt-8 border-t border-gray-200 flex justify-between">
                        <div class="text-center"><div class="border-b border-gray-400 w-48 mb-2"></div><span class="text-xs font-bold text-gray-500">Employee Signature</span></div>
                        <div class="text-center"><div class="border-b border-gray-400 w-48 mb-2"></div><span class="text-xs font-bold text-gray-500">HR / Admin Signature</span></div>
                    </div>
                </body>
            </html>
        `);
        win.document.close();
        setTimeout(() => {
            win.print();
        }, 500);
    }
"""

if "function initPayrollDropdown" not in content:
    content = content.replace("</script>", js_payroll + "\n</script>")
    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Payroll JS injected.")
else:
    print("Payroll JS already exists.")
