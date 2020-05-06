Enable/disable javascript for the root domain of a subdomain. For example,
enable javascript for *://*.qutebrowser.org when visiting
https://blog.qutebrowser.org.

Usage:
    :spawn --userscript qutejs.py [-t]

Arguments:
    -t: Set value temporarily until qutebrowser is closed.

Dependencies:
    qutejs requires tldextract.
