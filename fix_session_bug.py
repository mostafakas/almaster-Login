import re

def fix_session_bug(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove the undefined unsubscribeUser from loadUserProfile
    bad_code = "if (unsubscribeUser) unsubscribeUser();"
    if bad_code in content:
        content = content.replace(bad_code, "")
        print(f"Fixed ReferenceError in {filename}")
    
    # 2. Inject session check into onSnapshot (real-time kick)
    # The onSnapshot block looks like:
    #         userProfile = doc.data();
    #         if (timeReady && !resetInProgress && userProfile.dayKey && userProfile.dayKey !== getDayKey(serverNow())) { performReset('boundary'); return; }
    
    snapshot_search = r"(userProfile = doc\.data\(\);\s*)(if \(timeReady && !resetInProgress)"
    
    session_logic = """
            const localSession = localStorage.getItem('my_session_id');
            if (userProfile.sessionId && localSession && userProfile.sessionId !== localSession) {
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
            """
    
    # Check if we already injected it in onSnapshot
    if "Session Expired" not in re.search(r"userProfile = doc\.data\(\);(.*?)updateCentralUI", content, re.DOTALL).group(1):
        content = re.sub(snapshot_search, r"\1" + session_logic + r"\2", content)
        print(f"Added real-time session check to onSnapshot in {filename}")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

fix_session_bug('employee.html')
fix_session_bug('leader.html')
