"""Build deterministic independent skill ZIPs and a SHA-256 manifest."""
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build():
    config = json.loads((ROOT/'package.json').read_text(encoding='utf-8'))
    result = {'export_version': config['export_version'], 'repository': config['repository'], 'skills': []}
    (ROOT/'dist').mkdir(exist_ok=True)
    for folder in sorted((ROOT/'skills').iterdir()):
        if not (folder/'SKILL.md').is_file():
            continue
        files = sorted(p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
        content = (folder/'SKILL.md').read_text(encoding='utf-8')
        version = re.search(r'version: "([^"]+)"', content).group(1)
        archive = ROOT/'dist'/f'{folder.name}.zip'
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for path in files:
                info = zipfile.ZipInfo(path.relative_to(folder).as_posix(), date_time=(2026,11,1,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                z.writestr(info, path.read_bytes())
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            assert all(z.read(p.relative_to(folder).as_posix()) == p.read_bytes() for p in files)
        repo_slug = config['repository'].removeprefix('https://github.com/')
        entry = dict(name=folder.name, version=version, directory=f'skills/{folder.name}', zip_path=archive.relative_to(ROOT).as_posix(),
                     zip_url=f"https://github.com/{repo_slug}/blob/main/dist/{folder.name}.zip",
                     zip_sha256=digest(archive.read_bytes()),
                     files=[dict(path=p.relative_to(folder).as_posix(), sha256=digest(p.read_bytes()),
                                 url=f'https://raw.githubusercontent.com/{repo_slug}/main/skills/{folder.name}/{p.relative_to(folder).as_posix()}') for p in files])
        if config.get('public'):
            entry['zip_url'] = f'https://raw.githubusercontent.com/{repo_slug}/main/dist/{folder.name}.zip'
        result['skills'].append(entry)
    (ROOT/'manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'built': [x['name'] for x in result['skills']], 'verified_archives': len(result['skills'])}))


if __name__ == '__main__':
    build()
