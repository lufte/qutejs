#!/usr/bin/python3
import os, sys, urllib.parse, tldextract

"""
qutejs is a qutebrowser userscript that allows to enable javascript on a
per-domain basis. If you execute it, qutejs will take the current URL, extract
the domain from it (without subdomains) and make qutebrowser enable javascript
for that domain on every subdomain and path.

So, if the URL "https://maps.google.com.uy/path?query=value#hash" is provided,
this will enable javascript for "*.google.com.uy/*".

Installation:
    Place qutejs.py in your QUTE_DATA_DIR/userscripts/ directory.

    If you're using this userscript, the logical next step is to disable
    javascript in your config.py with:

    ```
    c.content.javascript.enabled = False
    ```

    Next, you will probably want to add some shortcuts to execute the script.

    ```
    config.bind(',ejp', 'spawn --userscript qutejs.py')
    config.bind(',ejt', 'spawn --userscript qutejs.py -t')
    ```

    If you want to remember patterns between sessions, place the following
    snippet in your config.py as well.

    ```
    from qutebrowser.utils import standarddir
    with open(os.path.join(standarddir.config(),
                           'javascript_enabled_patterns.txt')) as patterns:
        pattern = patterns.readline().strip()
        while pattern:
            config.set('content.javascript.enabled', True, pattern)
            pattern = patterns.readline().strip()
    ```
Usage:
    qutejs --userscript [-t] [url]
Arguments:
    -t: temporary mode. If used, qutejs will only make qutebrowser change the
      setting using ":set --pattern PATTERN content.javascript.enabled true".
      If not used, qutejs will also write the pattern to a file in your
      QUTE_CONFIG_DIR directory. It's your responsibility to load that file
      in your config.py, see the Installation instructions.
    url: The url for extracting the domain. If not passed, QUTE_URL will be
       used.
Dependencies:
    qutejs requires tldextract.
"""

def get_args(argv):
    """Parse shell arguments"""
    arguments = argv[1:]
    temp = '-t' in arguments
    if temp:
        arguments.remove('-t')
    url = arguments[0] if arguments else os.environ['QUTE_URL']
    return temp, url


if __name__ == '__main__':
    temp, url = get_args(sys.argv)
    domain_parts = urllib.parse.urlparse(url)[1].split(':', 1)
    if len(domain_parts) > 1:
        domain, port, *_ = domain_parts
    else:
        domain = domain_parts[0]
        port = None
    sld = '.'.join(p for p in tldextract.extract(domain)[1:] if p)
    assert sld, 'Malformed url'
    pattern = '*.{}{}/*'.format(sld, ':' + port if port else '')

    with open(os.environ['QUTE_FIFO'], 'w') as fifo:
        fifo.write('set --pattern {} content.javascript.enabled '
                   'true\n'.format(pattern))
        fifo.write('reload\n')

    if not temp:
        patterns_path = os.path.join(os.environ['QUTE_CONFIG_DIR'],
                                     'javascript_enabled_patterns.txt')
        with open(patterns_path, 'a') as patterns:
            patterns.write(pattern + '\n')
