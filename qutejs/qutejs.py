#!/usr/bin/python3
import os, sys, urllib.parse, tldextract


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
