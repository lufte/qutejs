#!/usr/bin/env python3

# Copyright 2018-2020 Javier Ayres
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Enable/disable javascript for the root domain of a subdomain. For example,
enable javascript for *://*.qutebrowser.org when visiting
https://blog.qutebrowser.org.

Usage:
    :spawn --userscript qutejs.py [-t]

Arguments:
    -t: Set value temporarily until qutebrowser is closed.

Dependencies:
    qutejs requires tldextract.
"""

import os, sys, urllib.parse, tldextract


if __name__ == '__main__':
    arguments = sys.argv[1:]
    temp = '-t' in arguments
    url = os.environ['QUTE_URL']
    domain_parts = urllib.parse.urlparse(url)[1].split(':', 1)
    if len(domain_parts) > 1:
        domain, port, *_ = domain_parts
    else:
        domain = domain_parts[0]
        port = None
    tld_result = tldextract.extract(domain)
    sld = '{}.{}'.format(tld_result.domain, tld_result.suffix)
    assert sld, 'Malformed url'
    pattern = '*://*.{}{}/*'.format(sld, ':' + port if port else '')

    with open(os.environ['QUTE_FIFO'], 'w') as fifo:
        if temp:
            fifo.write(
                'config-cycle -t -p -u {} '
                'content.javascript.enabled ;; reload'.format(pattern)
            )
        else:
            fifo.write(
                'config-cycle -p -u {} '
                'content.javascript.enabled ;; reload'.format(pattern)
            )

