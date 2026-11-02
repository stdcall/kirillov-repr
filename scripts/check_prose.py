"""Advisory Russian typography checks over the Typst sources."""
import json
import os
from pathlib import Path
import shutil
import subprocess

from project import ROOT, cache_path


def main():
    vale = os.environ.get('BOOK_VALE') or shutil.which('vale')
    parser = os.environ.get('BOOK_TYPST2VAST') or shutil.which('typst2vast')
    if not vale or not parser:
        raise SystemExit('The prose check requires vale and typst2vast.')
    sources = sorted((ROOT/'content').rglob('*.typ'))
    result = subprocess.run(
        [vale, '--config', str(ROOT/'checks/vale/.vale.ini'),
         '--output', 'JSON', *map(str, sources)],
        capture_output=True, text=True,
        env=dict(os.environ, PATH=str(Path(parser).parent) + os.pathsep
                 + os.environ.get('PATH', '')))
    if not result.stdout.strip() or 'typst2vast not found' in result.stderr:
        raise RuntimeError(result.stderr or 'Vale returned no report.')
    findings = json.loads(result.stdout)
    cache = cache_path()
    cache.mkdir(parents=True, exist_ok=True)
    (cache/'prose-vale.json').write_text(
        json.dumps(findings, ensure_ascii=False, indent=2)+'\n')
    count = 0
    for path, entries in findings.items():
        for entry in entries:
            count += 1
            print(f'{Path(path).name}:{entry["Line"]}: '
                  f'{entry["Check"]}: {entry["Message"]}')
    print(f'Vale: {count} findings (advisory).')


if __name__ == '__main__':
    main()
