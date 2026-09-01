import re

old_code = """        if (newStatus === 'Online') {
            const fo = userProfile.firstOnlineAt ? getMillis(userProfile.firstOnlineAt) : null;
            if (!fo || getDayKey(fo) !== getDayKey(sNow)) updates.firstOnlineAt = serverTs();
        }"""

new_code = """        if (newStatus === 'Online') {
            const fo = userProfile.firstOnlineAt ? getMillis(userProfile.firstOnlineAt) : null;
            if (!fo || getDayKey(fo) !== getDayKey(sNow)) {
                updates.firstOnlineAt = serverTs();
                
                // Grace Period Bonus Logic (9:00 to 9:30)
                const d = new Date(sNow);
                const timeInMins = d.getHours() * 60 + d.getMinutes();
                if (timeInMins >= 540 && timeInMins <= 570) {
                    const nineAM = new Date(d);
                    nineAM.setHours(9, 0, 0, 0);
                    const bonusMs = sNow - nineAM.getTime();
                    if (bonusMs > 0) {
                        bank['Online'] = (bank['Online'] || 0) + bonusMs;
                        updates.timeBank = bank;
                    }
                }
            }
        }"""

for filename in ['employee.html', 'leader.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")
    else:
        print(f"Code not found in {filename} or already updated.")
