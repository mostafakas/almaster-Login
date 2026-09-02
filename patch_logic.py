import re

def patch_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Enforce Session ID
    old_snapshot = """            userProfile = doc.data();
            await syncServerTime();
            await handleNewDayCheck(); """
    
    new_snapshot = """            const data = doc.data();
            const localSession = localStorage.getItem('my_session_id');
            if (data.sessionId && localSession && data.sessionId !== localSession) {
                if (unsubscribeUser) unsubscribeUser();
                Swal.fire({
                    icon: 'warning',
                    title: 'Session Expired',
                    text: 'You logged in from another device. This session will be closed.',
                    allowOutsideClick: false,
                    showConfirmButton: true,
                    confirmButtonText: 'Log out'
                }).then(() => {
                    auth.signOut().then(() => { window.location.replace('index.html'); });
                });
                return;
            }
            userProfile = data;
            await syncServerTime();
            await handleNewDayCheck(); """
    
    if old_snapshot in content:
        content = content.replace(old_snapshot, new_snapshot)
    else:
        print(f"Warning: Session ID patch not applied in {filename}")

    # 2. Force Offline on Boundary Reset
    old_boundary = """        if (reason === 'boundary') {
            updates.status = userProfile.status || 'Offline';
        }"""
    if old_boundary in content:
        content = content.replace(old_boundary, "")
    else:
        print(f"Warning: Boundary patch not applied in {filename}")

    # 3. Inject Grace Period into submitWorkLocation
    # Find the submitWorkLocation block
    old_submit = """        const updates = {
            status: 'Online',
            timeBank: Object.fromEntries(countedKeys().map(k => [k, 0])),
            lastChange: serverTs(),
            lastChangeClient: clientNow,
            dayKey: todayKey,
            firstOnlineAt: serverTs(),
            workLocation: type
        };"""
    
    new_submit = """        const sNow = new Date(Date.now() + serverOffset);
        const timeBank = Object.fromEntries(countedKeys().map(k => [k, 0]));
        
        // Grace Period Bonus Logic (9:00 to 9:30)
        const timeInMins = sNow.getHours() * 60 + sNow.getMinutes();
        if (timeInMins >= 540 && timeInMins <= 570) {
            const nineAM = new Date(sNow);
            nineAM.setHours(9, 0, 0, 0);
            const bonusMs = sNow.getTime() - nineAM.getTime();
            if (bonusMs > 0) {
                timeBank['Online'] = bonusMs;
            }
        }
        
        const updates = {
            status: 'Online',
            timeBank: timeBank,
            lastChange: serverTs(),
            lastChangeClient: clientNow,
            dayKey: todayKey,
            firstOnlineAt: serverTs(),
            workLocation: type
        };"""
    
    if old_submit in content:
        content = content.replace(old_submit, new_submit)
    else:
        print(f"Warning: submitWorkLocation patch not applied in {filename}")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filename} successfully.")

patch_file('employee.html')
patch_file('leader.html')
