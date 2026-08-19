import re

with open('leader.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('async function submitLeaveRequest(e) {')
end_idx = content.find('function restartLogsListener()', start_idx)

if start_idx != -1 and end_idx != -1:
    new_js = '''    async function submitLeaveRequest(e) {
        e.preventDefault();
        const btn = document.getElementById('btn-submit-leave');
        btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> جاري الإرسال...';
        try {
            await db.collection('leave_requests').add({
                user: EMAIL, name: userProfile.name || EMAIL,
                managerId: userProfile.leaderEmail || '',
                req_class: 'leave',
                type: document.getElementById('leave-type').value,
                target_date: document.getElementById('leave-date').value,
                reason: document.getElementById('leave-reason').value.trim(),
                status: 'pending', submitted_at: serverTs()
            });
            document.getElementById('leave-form').reset();
            document.getElementById('leave-date').value = zonedYMD(serverNow());
            showToast('Submitted', 'Your request is pending review.', 'success');
        } catch (err) { console.error(err); showToast('Could not submit', 'An error occurred.', 'error'); }
        btn.disabled = false; btn.innerHTML = 'إرسال للمدير المباشر';
        closeModal('modal-leave-request');
    }

    async function submitOnlineRequest(e) {
        e.preventDefault();
        const btn = document.getElementById('btn-submit-online');
        btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> جاري الإرسال...';
        try {
            await db.collection('leave_requests').add({
                user: EMAIL, name: userProfile.name || EMAIL,
                managerId: userProfile.leaderEmail || '',
                req_class: 'online',
                type: 'online_work',
                target_date: document.getElementById('online-date').value,
                reason: document.getElementById('online-reason').value.trim(),
                status: 'pending', submitted_at: serverTs()
            });
            document.getElementById('online-form').reset();
            document.getElementById('online-date').value = zonedYMD(serverNow());
            showToast('تم الإرسال', 'تم رفع طلب الأونلاين للمدير المباشر.', 'success');
        } catch (err) { console.error(err); showToast('خطأ', 'حدث خطأ أثناء الإرسال.', 'error'); }
        btn.disabled = false; btn.innerHTML = 'إرسال للمدير المباشر';
        closeModal('modal-online-request');
    }

    const LEAVE_LABELS = { sick:'Sick leave', annual:'Annual leave', excuse_late:'Late permission', excuse_early:'Early leave' };
    const LEAVE_STATUS = {
        pending: { t:'Pending', c:'bg-amber-50 text-amber-600 border-amber-100' },
        approved: { t:'Approved', c:'bg-emerald-50 text-emerald-600 border-emerald-100' },
        rejected: { t:'Rejected', c:'bg-red-50 text-red-600 border-red-100' }
    };

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

    function fetchTeamRequests() {
        if(window.unsubscribeTeamRequests) { return; }
        window.unsubscribeTeamRequests = db.collection('leave_requests').where('managerId', '==', EMAIL).where('status', '==', 'pending').onSnapshot(snap => {
            const box = document.getElementById('team-requests-container'); if (!box) return;
            if (snap.empty) { box.innerHTML = '<p class="text-xs text-textMuted italic text-center py-6">No pending team requests.</p>'; return; }
            const rows = []; snap.forEach(d => rows.push({id: d.id, ...d.data()}));
            rows.sort((a, b) => getMillis(b.submitted_at) - getMillis(a.submitted_at));
            box.innerHTML = rows.map(l => {
                const reqTitle = (l.req_class === 'online' ? 'طلب أونلاين' : (LEAVE_LABELS[l.type] || l.type));
                return `<div class="flex flex-col bg-slate-50 p-4 rounded-xl border border-slate-100 mb-3">
                    <div class="flex justify-between items-start w-full mb-3">
                        <div class="text-left flex-1">
                            <p class="text-xs font-black text-brand-navy">${l.name} <span class="text-textMuted font-medium">requested</span> ${reqTitle}</p>
                            <p class="text-[10px] font-bold text-textMuted mt-1"><i class="far fa-calendar-alt me-1"></i>${l.target_date || ''}</p>
                            ${l.reason ? `<p class="text-[10px] font-medium text-slate-600 mt-2 p-2 bg-white rounded border border-slate-200">${l.reason}</p>` : ''}
                        </div>
                    </div>
                    <div class="flex gap-2 w-full mt-2 border-t border-slate-200 pt-3">
                        <button onclick="handleTeamReq('${l.id}', 'approved', '${l.type}', '${l.user}')" class="flex-1 bg-emerald-500 text-white py-2 rounded-lg text-xs font-bold hover:bg-emerald-600 transition"><i class="fas fa-check me-1"></i> Approve</button>
                        <button onclick="handleTeamReq('${l.id}', 'rejected', '${l.type}', '${l.user}')" class="flex-1 bg-red-500 text-white py-2 rounded-lg text-xs font-bold hover:bg-red-600 transition"><i class="fas fa-times me-1"></i> Reject</button>
                    </div>
                </div>`;
            }).join('');
        }, err => console.warn('team requests:', err.message));
    }

    window.handleTeamReq = async (id, newStatus, type, userEmail) => {
        try {
            await db.collection('leave_requests').doc(id).update({
                status: newStatus, reviewed_at: serverTs(), reviewed_by: userProfile.name || EMAIL
            });
            
            if (newStatus === 'approved' && type === 'annual' && userEmail) {
                const ref = db.collection('hr_stats').doc(userEmail.toLowerCase().trim());
                await ref.set({ annualLeavesLeft: firebase.firestore.FieldValue.increment(-1) }, { merge:true });
            }
            
            showToast('Success', 'Request ' + newStatus, 'success');
        } catch(e) {
            console.error(e);
            showToast('Error', 'Failed to update request', 'error');
        }
    };
    
'''
    
    content = content[:start_idx] + new_js + content[end_idx:]
    
    content = content.replace('listenToMyLeaves();', 'fetchMyRequests();')
    
    with open('leader.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("leader.html updated successfully!")
else:
    print("Could not find insertion points in leader.html")

