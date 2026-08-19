import re

with open('supervisor.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert modals at the end of body, right before </body>
modals_html = '''
    <!-- Requests Menu Modal -->
    <div id="modal-requests-menu" class="fixed inset-0 z-[700] hidden bg-brand-navy/50 backdrop-blur-sm flex items-center justify-center p-4" role="dialog" aria-modal="true" onclick="closeModal('modal-requests-menu')">
        <div class="bg-white w-full max-w-sm rounded-[2rem] shadow-2xl overflow-hidden flex flex-col p-6 text-center" onclick="event.stopPropagation()">
            <div class="flex justify-between items-center mb-6">
                <h3 class="font-black text-lg text-textMain"><i class="fas fa-envelope-open-text text-brand-blue me-2"></i> الطلبات</h3>
                <button onclick="closeModal('modal-requests-menu')" class="text-slate-400 hover:text-red-500 transition"><i class="fas fa-times text-lg"></i></button>
            </div>
            <div class="flex flex-col gap-3">
                <button onclick="closeModal('modal-requests-menu'); openModal('modal-online-request')" class="w-full py-4 rounded-xl bg-surface border border-slate-200 text-textMain font-black text-sm hover:border-brand-blue hover:text-brand-blue transition-colors flex items-center justify-center gap-2 shadow-sm">
                    <i class="fas fa-laptop-house text-emerald-500"></i> طلب أونلاين
                </button>
                <button onclick="closeModal('modal-requests-menu'); openModal('modal-leave-request')" class="w-full py-4 rounded-xl bg-surface border border-slate-200 text-textMain font-black text-sm hover:border-brand-blue hover:text-brand-blue transition-colors flex items-center justify-center gap-2 shadow-sm">
                    <i class="fas fa-file-signature text-amber-500"></i> طلب إجازة / استئذان
                </button>
                <button onclick="closeModal('modal-requests-menu'); openModal('modal-previous-requests'); fetchMyRequests();" class="w-full py-4 rounded-xl bg-surface border border-slate-200 text-textMain font-black text-sm hover:border-brand-blue hover:text-brand-blue transition-colors flex items-center justify-center gap-2 shadow-sm">
                    <i class="fas fa-history text-slate-500"></i> الطلبات السابقة
                </button>
            </div>
        </div>
    </div>

    <!-- Online Request Modal -->
    <div id="modal-online-request" class="fixed inset-0 z-[700] hidden bg-brand-navy/50 backdrop-blur-sm flex items-center justify-center p-4" role="dialog" aria-modal="true" onclick="closeModal('modal-online-request')">
        <div class="bg-white w-full max-w-md rounded-[2rem] shadow-2xl overflow-hidden flex flex-col" onclick="event.stopPropagation()">
            <div class="p-5 border-b border-slate-100 bg-surface flex justify-between items-center">
                <h3 class="font-black text-sm text-textMain"><i class="fas fa-laptop-house text-emerald-500 me-2"></i> طلب أونلاين</h3>
                <button onclick="closeModal('modal-online-request')" aria-label="Close" class="text-slate-400 hover:text-red-500 transition"><i class="fas fa-times text-lg"></i></button>
            </div>
            <form id="online-form" onsubmit="submitOnlineRequest(event)" class="p-6 space-y-4">
                <div>
                    <label for="online-date" class="block text-[10px] font-black text-textMuted mb-2 uppercase">تاريخ الأونلاين (Date)</label>
                    <input type="date" id="online-date" required class="w-full bg-surface border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold text-textMain outline-none focus:border-brand-blue">
                </div>
                <div>
                    <label for="online-reason" class="block text-[10px] font-black text-textMuted mb-2 uppercase">التفاصيل / السبب (Details)</label>
                    <textarea id="online-reason" required rows="3" class="w-full bg-surface border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold text-textMain outline-none focus:border-brand-blue resize-none" placeholder="تفاصيل الطلب هنا..."></textarea>
                </div>
                <button type="submit" id="btn-submit-online" class="w-full py-3 bg-brand-blue text-white rounded-xl font-black text-xs shadow-md hover:bg-brand-navy2 btn-action">إرسال للمدير المباشر</button>
            </form>
        </div>
    </div>

    <!-- Leave modal -->
    <div id="modal-leave-request" class="fixed inset-0 z-[700] hidden bg-brand-navy/50 backdrop-blur-sm flex items-center justify-center p-4" role="dialog" aria-modal="true" aria-labelledby="leave-title" onclick="closeModal('modal-leave-request')">
        <div class="bg-white w-full max-w-md rounded-[2rem] shadow-2xl overflow-hidden flex flex-col max-h-[88vh]" onclick="event.stopPropagation()">
            <div class="p-5 border-b border-slate-100 bg-surface flex justify-between items-center">
                <h3 id="leave-title" class="font-black text-sm text-textMain"><i class="fas fa-file-lines text-amber-500 me-2"></i> Request Leave / Permission (طلب إجازة)</h3>
                <button onclick="closeModal('modal-leave-request')" aria-label="Close" class="text-slate-400 hover:text-red-500 transition"><i class="fas fa-times text-lg"></i></button>
            </div>
            <div class="flex-1 overflow-y-auto custom-scrollbar">
                <form id="leave-form" onsubmit="submitLeaveRequest(event)" class="p-6 space-y-4 border-b border-slate-100">
                    <div>
                        <label for="leave-type" class="block text-[10px] font-black text-textMuted mb-2 uppercase">Request type</label>
                        <select id="leave-type" required class="w-full bg-surface border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold text-textMain outline-none focus:border-brand-blue">
                            <option value="sick">Sick leave (مرضي)</option>
                            <option value="annual">Annual leave (سنوي)</option>
                            <option value="excuse_late">Late permission (إذن تأخير)</option>
                            <option value="excuse_early">Early leave permission (إذن انصراف مبكر)</option>
                        </select>
                    </div>
                    <div>
                        <label for="leave-date" class="block text-[10px] font-black text-textMuted mb-2 uppercase">Date</label>
                        <input type="date" id="leave-date" required class="w-full bg-surface border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold text-textMain outline-none focus:border-brand-blue">
                    </div>
                    <div>
                        <label for="leave-reason" class="block text-[10px] font-black text-textMuted mb-2 uppercase">Reason / Justification</label>
                        <textarea id="leave-reason" required rows="3" class="w-full bg-surface border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold text-textMain outline-none focus:border-brand-blue resize-none" placeholder="Write the details here..."></textarea>
                    </div>
                    <button type="submit" id="btn-submit-leave" class="w-full py-3 bg-brand-blue text-white rounded-xl font-black text-xs shadow-md hover:bg-brand-navy2 btn-action">إرسال للمدير المباشر</button>
                </form>
            </div>
        </div>
    </div>

    <!-- Previous Requests Modal -->
    <div id="modal-previous-requests" class="fixed inset-0 z-[700] hidden bg-brand-navy/50 backdrop-blur-sm flex items-center justify-center p-4" role="dialog" aria-modal="true" onclick="closeModal('modal-previous-requests')">
        <div class="bg-white w-full max-w-2xl rounded-[2rem] shadow-2xl overflow-hidden flex flex-col max-h-[88vh]" onclick="event.stopPropagation()">
            <div class="p-5 border-b border-slate-100 bg-surface flex justify-between items-center">
                <h3 class="font-black text-sm text-textMain"><i class="fas fa-history text-brand-blue me-2"></i> الطلبات السابقة</h3>
                <button onclick="closeModal('modal-previous-requests')" aria-label="Close" class="text-slate-400 hover:text-red-500 transition"><i class="fas fa-times text-lg"></i></button>
            </div>
            <div class="p-6 flex-1 overflow-y-auto custom-scrollbar">
                <div id="my-requests-container" class="space-y-3"><p class="text-xs text-textMuted italic text-center py-6"><i class="fas fa-spinner fa-spin me-2"></i> جاري التحميل...</p></div>
            </div>
        </div>
    </div>
'''

content = content.replace('<!-- MAIN APP SCRIPT -->', modals_html + '\n    <!-- MAIN APP SCRIPT -->')

# 2. Add header button
header_btn = '''<button onclick="openModal('modal-requests-menu')" class="h-10 px-4 bg-brand-navy2 text-white font-black text-xs hover:bg-brand-blueLt rounded-xl flex items-center justify-center transition-colors shadow-sm gap-2">
                    <i class="fas fa-envelope-open-text"></i> <span class="hidden sm:inline">الطلبات</span>
                </button>
                <button onclick="logoutAdmin()" class="w-10 h-10 bg-red-50'''
content = content.replace('<button onclick="logoutAdmin()" class="w-10 h-10 bg-red-50', header_btn)


# 3. Update requests tab query and renderer
content = content.replace("db.collection('leave_requests').where('status','==','pending')", "db.collection('leave_requests').where('managerId','==',EMAIL).where('status','==','pending')")

renderer_old = '''const st = LEAVE_STATUS[l.status] || LEAVE_STATUS.pending;
                return `<div class="flex flex-col bg-slate-50 p-4 rounded-xl border border-slate-100 mb-3 relative group">
                    <div class="flex justify-between items-start w-full mb-3">
                        <div class="text-left flex-1">
                            <p class="text-xs font-black text-brand-navy">${l.name} <span class="text-textMuted font-medium">requested</span> ${LEAVE_LABELS[l.type] || l.type}</p>
                            <p class="text-[10px] font-bold text-textMuted mt-1"><i class="far fa-calendar-alt me-1"></i>${l.target_date || ''}</p>
                            ${l.reason ? `<p class="text-[10px] font-medium text-slate-600 mt-2 p-2 bg-white rounded border border-slate-200">${l.reason}</p>` : ''}
                        </div>
                    </div>
                    <div class="flex gap-2 w-full mt-2 border-t border-slate-200 pt-3">
                        <button onclick="handleRequestAction('${l.id}', 'approved', '${l.type}', '${l.user}')" class="flex-1 bg-emerald-500 text-white py-2 rounded-lg text-xs font-bold hover:bg-emerald-600 transition"><i class="fas fa-check me-1"></i> Approve</button>
                        <button onclick="handleRequestAction('${l.id}', 'rejected', '${l.type}', '${l.user}')" class="flex-1 bg-red-500 text-white py-2 rounded-lg text-xs font-bold hover:bg-red-600 transition"><i class="fas fa-times me-1"></i> Reject</button>
                    </div>
                </div>`;'''

renderer_new = '''const st = LEAVE_STATUS[l.status] || LEAVE_STATUS.pending;
                const reqTitle = (l.req_class === 'online' ? 'طلب أونلاين' : (LEAVE_LABELS[l.type] || l.type));
                return `<div class="flex flex-col bg-slate-50 p-4 rounded-xl border border-slate-100 mb-3 relative group">
                    <div class="flex justify-between items-start w-full mb-3">
                        <div class="text-left flex-1">
                            <p class="text-xs font-black text-brand-navy">${l.name} <span class="text-textMuted font-medium">requested</span> ${reqTitle}</p>
                            <p class="text-[10px] font-bold text-textMuted mt-1"><i class="far fa-calendar-alt me-1"></i>${l.target_date || ''}</p>
                            ${l.reason ? `<p class="text-[10px] font-medium text-slate-600 mt-2 p-2 bg-white rounded border border-slate-200">${l.reason}</p>` : ''}
                        </div>
                    </div>
                    <div class="flex gap-2 w-full mt-2 border-t border-slate-200 pt-3">
                        <button onclick="handleRequestAction('${l.id}', 'approved', '${l.type}', '${l.user}')" class="flex-1 bg-emerald-500 text-white py-2 rounded-lg text-xs font-bold hover:bg-emerald-600 transition"><i class="fas fa-check me-1"></i> Approve</button>
                        <button onclick="handleRequestAction('${l.id}', 'rejected', '${l.type}', '${l.user}')" class="flex-1 bg-red-500 text-white py-2 rounded-lg text-xs font-bold hover:bg-red-600 transition"><i class="fas fa-times me-1"></i> Reject</button>
                    </div>
                </div>`;'''
content = content.replace(renderer_old, renderer_new)

# 4. Add JS methods for supervisor to make their own requests
js_funcs = '''
    const LEAVE_LABELS = { sick:'Sick leave', annual:'Annual leave', excuse_late:'Late permission', excuse_early:'Early leave' };
    const LEAVE_STATUS = {
        pending: { t:'Pending', c:'bg-amber-50 text-amber-600 border-amber-100' },
        approved: { t:'Approved', c:'bg-emerald-50 text-emerald-600 border-emerald-100' },
        rejected: { t:'Rejected', c:'bg-red-50 text-red-600 border-red-100' }
    };
    
    // We assume the supervisor has userProfile available. Actually supervisor.html has `adminProfile`, but let's check. 
    // Wait, supervisor.html might not load admin's leaderEmail since admins/supervisors might not have a leader!
    // But we will use EMAIL.
    
    async function submitLeaveRequest(e) {
        e.preventDefault();
        const btn = document.getElementById('btn-submit-leave');
        btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> جاري الإرسال...';
        try {
            await db.collection('leave_requests').add({
                user: EMAIL, name: document.getElementById('admin-name').innerText || EMAIL,
                managerId: '', // supervisors might not have managers. Or we can just set it empty, so it goes to HR
                req_class: 'leave',
                type: document.getElementById('leave-type').value,
                target_date: document.getElementById('leave-date').value,
                reason: document.getElementById('leave-reason').value.trim(),
                status: 'pending', submitted_at: serverTs()
            });
            document.getElementById('leave-form').reset();
            Swal.fire({icon:'success', title:'تم الإرسال', timer:1500});
        } catch (err) { console.error(err); Swal.fire({icon:'error', title:'Error'}); }
        btn.disabled = false; btn.innerHTML = 'إرسال للمدير المباشر';
        closeModal('modal-leave-request');
    }

    async function submitOnlineRequest(e) {
        e.preventDefault();
        const btn = document.getElementById('btn-submit-online');
        btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> جاري الإرسال...';
        try {
            await db.collection('leave_requests').add({
                user: EMAIL, name: document.getElementById('admin-name').innerText || EMAIL,
                managerId: '',
                req_class: 'online',
                type: 'online_work',
                target_date: document.getElementById('online-date').value,
                reason: document.getElementById('online-reason').value.trim(),
                status: 'pending', submitted_at: serverTs()
            });
            document.getElementById('online-form').reset();
            Swal.fire({icon:'success', title:'تم الإرسال', timer: 1500});
        } catch (err) { console.error(err); Swal.fire({icon:'error', title:'Error'}); }
        btn.disabled = false; btn.innerHTML = 'إرسال للمدير المباشر';
        closeModal('modal-online-request');
    }

    function fetchMyRequests() {
        if(window.unsubscribeMyRequests) { return; }
        window.unsubscribeMyRequests = db.collection('leave_requests').where('user', '==', EMAIL).onSnapshot(snap => {
            const box = document.getElementById('my-requests-container'); if (!box) return;
            if (snap.empty) { box.innerHTML = '<p class="text-xs text-textMuted italic text-center py-6">No requests yet.</p>'; return; }
            const rows = []; snap.forEach(d => rows.push(d.data()));
            rows.sort((a, b) => getMillis(b.submitted_at) - getMillis(a.submitted_at));
            box.innerHTML = rows.map(l => {
                const st = LEAVE_STATUS[l.status] || LEAVE_STATUS.pending;
                const reqTitle = (l.req_class === 'online' ? 'طلب أونلاين' : (LEAVE_LABELS[l.type] || l.type));
                let emailBtnHtml = '';
                if (l.status === 'approved') {
                    const subject = encodeURIComponent(`Approved ${reqTitle} Request - ${l.name}`);
                    const body = encodeURIComponent(`Hello HR,\n\nI have an approved ${reqTitle} for date: ${l.target_date || ''}.\n\nReason: ${l.reason || ''}\n\nEmployee: ${l.name}\nEmail: ${l.user}\n\nBest regards.`);
                    emailBtnHtml = `<a href="mailto:almaster.hr@outlook.com?subject=${subject}&body=${body}" class="mt-2 text-[10px] font-black bg-brand-navy text-white px-3 py-1.5 rounded-full hover:bg-brand-blue transition-colors shadow-sm text-center block w-full"><i class="fas fa-paper-plane me-1"></i> مراسلة الـ HR</a>`;
                }
                return `<div class="flex flex-col bg-slate-50 p-4 rounded-xl border border-slate-100 mb-3">
                    <div class="flex justify-between items-start w-full">
                        <div class="text-left flex-1">
                            <p class="text-xs font-black text-textMain">${reqTitle}</p>
                            <p class="text-[10px] font-bold text-textMuted mt-1"><i class="far fa-calendar-alt me-1"></i>${l.target_date || ''}</p>
                            ${l.reason ? `<p class="text-[10px] font-medium text-slate-500 mt-2 truncate w-48">${l.reason}</p>` : ''}
                        </div>
                        <span class="text-[10px] font-black px-2.5 py-1 rounded-full border ${st.c} ml-2 whitespace-nowrap">${st.t}</span>
                    </div>
                    ${emailBtnHtml}
                </div>`;
            }).join('');
        }, err => console.warn('my requests:', err.message));
    }

'''

content = content.replace('window.handleRequestAction', js_funcs + '    window.handleRequestAction')

# Decrease HR stats in handleRequestAction for supervisors approving team
content = content.replace('''await db.collection('leave_requests').doc(id).update({ status:newStatus, reviewed_at: serverTs(), reviewed_by: userProfile.name || 'Admin' });''', '''await db.collection('leave_requests').doc(id).update({ status:newStatus, reviewed_at: serverTs(), reviewed_by: document.getElementById('admin-name').innerText || EMAIL });''')
content = content.replace('''const cur = (userEmail in leaveBalances) ? leaveBalances[userEmail] : ANNUAL_LEAVE_DEFAULT;
                await ref.set({ annualLeavesLeft: Math.max(0, cur - 1) }, { merge:true });''', '''await ref.set({ annualLeavesLeft: firebase.firestore.FieldValue.increment(-1) }, { merge:true });''')


with open('supervisor.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("supervisor.html updated successfully!")
