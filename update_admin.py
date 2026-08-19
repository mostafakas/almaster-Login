import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change the query to approved
content = content.replace("db.collection('leave_requests').where('status','==','pending')", "db.collection('leave_requests').where('status','==','approved')")

# 2. Update the text in the empty state
content = content.replace("All caught up! No pending requests.", "No approved requests yet.")

# 3. Update the request card HTML
old_card = '''return <div class="bg-white p-5 rounded-3xl border border-slate-100 shadow-sm space-y-3 relative hover:shadow-md transition-shadow">
                    <div class="flex items-center gap-3">
                        <img src="" class="w-10 h-10 rounded-full bg-slate-50 border border-slate-100 object-cover">
                        <div>
                            <h4 class="font-black text-sm text-textMain"></h4>
                            <p class="text-[10px] font-bold text-textMuted uppercase tracking-wider"></p>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-[10px] font-black text--700 bg--50 px-2.5 py-1 rounded-md border border--100 shadow-sm"><i class="fas fa-tag mr-1"></i> </span>
                        <span class="text-[10px] font-black text-slate-600 bg-slate-100 px-2.5 py-1 rounded-md border border-slate-200 shadow-sm"><i class="far fa-calendar-alt mr-1"></i> </span>
                    </div>
                    <p class="text-xs text-textMain bg-surface p-3 rounded-xl border border-slate-100 font-medium leading-relaxed shadow-inner">""</p>
                    <div class="flex gap-2 w-full mt-2 pt-2 border-t border-slate-100">
                        <button onclick="processRequest('', 'approved', '', '')" class="flex-1 bg-emerald-500 text-white py-2 rounded-xl text-xs font-bold hover:bg-emerald-600 transition shadow-sm btn-action"><i class="fas fa-check me-1"></i> Approve</button>
                        <button onclick="processRequest('', 'rejected', '', '')" class="flex-1 bg-red-500 text-white py-2 rounded-xl text-xs font-bold hover:bg-red-600 transition shadow-sm btn-action"><i class="fas fa-times me-1"></i> Reject</button>
                    </div>
                </div>;'''

new_card = '''const reqTitle = (d.req_class === 'online' ? 'طلب أونلاين' : m.label);
                return <div class="bg-white p-5 rounded-3xl border border-slate-100 shadow-sm space-y-3 relative hover:shadow-md transition-shadow">
                    <div class="flex items-center gap-3">
                        <img src="" class="w-10 h-10 rounded-full bg-slate-50 border border-slate-100 object-cover">
                        <div>
                            <h4 class="font-black text-sm text-textMain"></h4>
                            <p class="text-[10px] font-bold text-textMuted uppercase tracking-wider"></p>
                        </div>
                    </div>
                    <div class="flex items-center gap-2 flex-wrap">
                        <span class="text-[10px] font-black text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-100 shadow-sm"><i class="fas fa-check-circle mr-1"></i> تمت الموافقة بواسطة: </span>
                        <span class="text-[10px] font-black text--700 bg--50 px-2.5 py-1 rounded-md border border--100 shadow-sm"><i class="fas fa-tag mr-1"></i> </span>
                        <span class="text-[10px] font-black text-slate-600 bg-slate-100 px-2.5 py-1 rounded-md border border-slate-200 shadow-sm"><i class="far fa-calendar-alt mr-1"></i> </span>
                    </div>
                    <p class="text-xs text-textMain bg-surface p-3 rounded-xl border border-slate-100 font-medium leading-relaxed shadow-inner">""</p>
                </div>;'''

# Fallback string replace just in case the multi-line string has different indentation
import re
content = re.sub(r'return <div class="bg-white p-5 rounded-3xl border border-slate-100 shadow-sm.*?</div>;', new_card, content, flags=re.DOTALL)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("admin.html updated successfully!")
