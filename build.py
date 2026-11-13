#!/usr/bin/env python3
"""Inline the vendored libraries and icons into one self-contained incognote.html."""
import json, pathlib

here = pathlib.Path(__file__).parent
src = (here / 'src/app.html').read_text(encoding='utf-8')
icons = json.loads((here / 'src/icons.json').read_text(encoding='utf-8'))
need = ['chevron.right', 'chevron.down', 'chevron.up.chevron.down', 'plus', 'magnifyingglass', 'folder', 'tray', 'clock',
        'doc', 'photo', 'ellipsis', 'lock', 'xmark', 'checkmark']
out = (src
       .replace('/*@@ICONS@@*/', json.dumps({k: icons[k] for k in need}, ensure_ascii=False))
       .replace('/*@@MDIT@@*/', (here / 'src/vendor/markdown-it.min.js').read_text(encoding='utf-8'))
       .replace('/*@@PURIFY@@*/', (here / 'src/vendor/purify.min.js').read_text(encoding='utf-8')))
assert '@@' not in out.split('<script>"use strict";')[0][-200:], 'placeholder left'
(here / 'incognote.html').write_text(out, encoding='utf-8')
print('incognote.html', len(out.encode('utf-8')), 'bytes')
