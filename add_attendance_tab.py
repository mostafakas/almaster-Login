import re

def add_attendance_tab():
    filename = 'admin.html'
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add Sidebar Button
    nav_attendance = """
            <button onclick="switchTab('attendance')" id="nav-attendance" class="nav-link text-textMuted w-full flex items-center gap-4 px-3 py-3.5 rounded-xl font-black text-xs transition-all hover:bg-brand-soft hover:text-brand-blue group/item">
                <i class="fas fa-calendar-check text-lg text-center w-6 shrink-0 group-hover/item:scale-110 transition-transform text-emerald-500"></i> 
                <span class="whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-300 delay-75">Daily Attendance</span>
            </button>
"""
    if 'id="nav-attendance"' not in content:
        content = content.replace('id="nav-payroll"', nav_attendance + '\n            <button onclick="switchTab(\'payroll\')" id="nav-payroll"')

    # 2. Add Tab Container
    tab_attendance = """
        <!-- Attendance Tab -->
        <div id="tab-attendance" class="hidden flex-1 flex-col h-full overflow-hidden">
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
                <div class="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="w-full text-left border-collapse">
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
    if 'id="tab-attendance"' not in content:
        content = content.replace('<!-- hr tab ends -->', '<!-- hr tab ends -->\n' + tab_attendance)
        # Just in case, let's insert it before <div id="tab-requests"
        if tab_attendance not in content:
            content = content.replace('<div id="tab-requests"', tab_attendance + '\n        <div id="tab-requests"')

    # 3. Add JS Logic
    js_logic = """
    // --- Attendance Logic ---
    async function loadAttendance() {
        const dateInput = document.getElementById('att-date-picker').value;
        if (!dateInput) return;
        const tbody = document.getElementById('attendance-tbody');
        tbody.innerHTML = '<tr><td colspan="6" class="px-6 py-10 text-center"><i class="fas fa-circle-notch fa-spin text-brand-blue text-2xl"></i></td></tr>';

        try {
            // Fetch logs for the day
            const logsSnap = await db.collection('logs').where('dayKey', '==', dateInput).get();
            const logsByUser = {};
            logsSnap.forEach(doc => {
                const d = doc.data();
                if (!logsByUser[d.user]) logsByUser[d.user] = [];
                logsByUser[d.user].push(d);
            });

            // Fetch overrides (Leave / Absent)
            const overridesSnap = await db.collection('attendance_override').where('dayKey', '==', dateInput).get();
            const overrides = {};
            overridesSnap.forEach(doc => {
                overrides[doc.data().user] = doc.data();
            });

            let rowsHtml = '';
            for (const user of allUsersData) {
                if (user.role === 'admin') continue;

                const email = user.email || user.id;
                const userLogs = logsByUser[email] || [];
                const override = overrides[email];
                
                let timeIn = '-';
                let timeOut = '-';
                let isLate = false;
                let status = 'No Record';
                let badgeClass = 'bg-slate-100 text-slate-500';

                if (userLogs.length > 0) {
                    userLogs.sort((a,b) => getMillis(a.timestamp) - getMillis(b.timestamp));
                    // First online log
                    const firstLog = userLogs.find(l => l.to_status === 'Online' || l.to_status === 'Office' || l.to_status === 'Remote');
                    if (firstLog) {
                        const ms = getMillis(firstLog.timestamp);
                        timeIn = fmtTime(ms);
                        // Check if late (after 9:30 AM)
                        const d = new Date(ms);
                        const mins = d.getHours() * 60 + d.getMinutes();
                        if (mins > 570) isLate = true; // 9:30 AM = 570 mins
                    }
                    // Last log
                    const lastLog = userLogs[userLogs.length - 1];
                    timeOut = fmtTime(getMillis(lastLog.timestamp));
                    
                    status = 'Present';
                    badgeClass = 'bg-emerald-50 text-emerald-600 border border-emerald-100';
                }

                if (override) {
                    status = override.status; // 'Absent' or 'Leave'
                    if (status === 'Absent') badgeClass = 'bg-red-50 text-red-600 border border-red-100';
                    if (status === 'Leave') badgeClass = 'bg-amber-50 text-amber-600 border border-amber-100';
                }

                const lateBadge = isLate 
                    ? '<span class="px-2 py-0.5 bg-rose-50 text-rose-600 rounded-full text-[10px]">Late</span>' 
                    : '<span class="px-2 py-0.5 bg-slate-50 text-slate-400 rounded-full text-[10px]">-</span>';

                rowsHtml += `
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="px-6 py-4">
                            <div class="flex items-center gap-3">
                                <img src="${getAvatar(user)}" class="w-8 h-8 rounded-xl object-cover border border-slate-200">
                                <div>
                                    <p class="text-xs font-black">${user.name}</p>
                                    <p class="text-[9px] text-textMuted">${user.title || ''}</p>
                                </div>
                            </div>
                        </td>
                        <td class="px-6 py-4">
                            <span class="px-3 py-1 rounded-full text-[10px] font-black ${badgeClass}">${status}</span>
                        </td>
                        <td class="px-6 py-4 tabular-nums text-xs">${timeIn}</td>
                        <td class="px-6 py-4 tabular-nums text-xs">${timeOut}</td>
                        <td class="px-6 py-4">${lateBadge}</td>
                        <td class="px-6 py-4 text-right">
                            <button onclick="setAttendanceOverride('${email}', '${dateInput}', 'Absent')" class="text-[10px] font-black px-3 py-1.5 rounded-lg bg-red-50 text-red-600 hover:bg-red-100 transition-colors mr-1">Mark Absent</button>
                            <button onclick="setAttendanceOverride('${email}', '${dateInput}', 'Leave')" class="text-[10px] font-black px-3 py-1.5 rounded-lg bg-amber-50 text-amber-600 hover:bg-amber-100 transition-colors mr-1">Mark Leave</button>
                            <button onclick="setAttendanceOverride('${email}', '${dateInput}', 'Clear')" class="text-[10px] font-black px-3 py-1.5 rounded-lg bg-slate-100 text-slate-500 hover:bg-slate-200 transition-colors" title="Clear Override"><i class="fas fa-times"></i></button>
                        </td>
                    </tr>
                `;
            }
            
            tbody.innerHTML = rowsHtml || '<tr><td colspan="6" class="px-6 py-10 text-center text-xs text-textMuted">No employees found.</td></tr>';

        } catch (e) {
            console.error(e);
            tbody.innerHTML = '<tr><td colspan="6" class="px-6 py-10 text-center text-xs text-red-500">Error loading data.</td></tr>';
        }
    }

    async function setAttendanceOverride(email, dayKey, newStatus) {
        try {
            const docId = email + '_' + dayKey;
            const ref = db.collection('attendance_override').doc(docId);
            const doc = await ref.get();
            const oldStatus = doc.exists ? doc.data().status : null;
            
            if (newStatus === 'Clear') {
                if (doc.exists) await ref.delete();
            } else {
                await ref.set({ user: email, dayKey, status: newStatus, timestamp: serverTs() });
            }

            // Adjust Leaves Balance if changing to/from "Leave"
            if (newStatus === 'Leave' && oldStatus !== 'Leave') {
                const statRef = db.collection('hr_stats').doc(email);
                const stat = await statRef.get();
                if (stat.exists && typeof stat.data().annualLeavesLeft === 'number') {
                    await statRef.update({ annualLeavesLeft: firebase.firestore.FieldValue.increment(-1) });
                }
            } else if (oldStatus === 'Leave' && newStatus !== 'Leave') {
                const statRef = db.collection('hr_stats').doc(email);
                const stat = await statRef.get();
                if (stat.exists && typeof stat.data().annualLeavesLeft === 'number') {
                    await statRef.update({ annualLeavesLeft: firebase.firestore.FieldValue.increment(1) });
                }
            }

            showToast('Success', `Attendance updated for ${email}`, 'success');
            loadAttendance();
            
        } catch (e) {
            console.error(e);
            showToast('Error', 'Could not update attendance', 'error');
        }
    }

    // Default Date for DatePicker
    document.addEventListener('DOMContentLoaded', () => {
        const picker = document.getElementById('att-date-picker');
        if (picker) {
            picker.value = zonedYMD(serverNow());
        }
    });
    // --- End Attendance Logic ---
"""
    if 'loadAttendance()' not in content:
        content = content.replace('</script>', js_logic + '\n</script>', 1)
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Done adding attendance tab.")

add_attendance_tab()
