import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

global_funcs = '''
    window.toggleLeaderDropdown = function() {
        document.getElementById('u-leader-dropdown').classList.toggle('hidden');
    };
    
    window.selectLeader = function(email, name, avatarUrl) {
        document.getElementById('u-leader-email').value = email;
        const btn = document.getElementById('u-leader-selected-content');
        if (!email) {
            btn.innerHTML = <span class="text-slate-500 text-xs">None (Direct to Admin/Supervisor)</span>;
        } else {
            btn.innerHTML = <img src="" class="w-6 h-6 rounded-full object-cover border border-slate-200 shadow-sm shrink-0"> <span class="text-brand-navy text-xs font-black truncate"></span>;
        }
        document.getElementById('u-leader-dropdown').classList.add('hidden');
    };
    
    document.addEventListener('click', function(e) {
        const dd = document.getElementById('u-leader-dropdown');
        const btn = document.getElementById('u-leader-select-btn');
        if (dd && !dd.classList.contains('hidden') && !dd.contains(e.target) && !btn.contains(e.target)) {
            dd.classList.add('hidden');
        }
    });
'''

# insert right before the closing </script>
content = content.replace('</script>\n</body>', global_funcs + '\n</script>\n</body>')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Added selectLeader functions!")
