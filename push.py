import argparse
import os.path
import subprocess
import sys
import tempfile
from typing import Tuple


def lang_pkg(lang: str, pkg: str) -> Tuple[str, ...]:
    return (f'--language={lang}', f'--package-name={pkg}')


CSS = '--types=css'
JS = '--types=javascript'
PP = '--types=puppet'
PY = '--types=python'
RB = '--types=ruby'
SCSS = '--types=scss'

REPOS = (
    ('mirrors-autopep8', *lang_pkg('python', 'autopep8'), PY, '--args=-i'),
    (
        'mirrors-coffeelint',
        *lang_pkg('node', 'coffeelint'), r'--files-regex=\.(js|coffee)$',
    ),
    ('mirrors-csslint', *lang_pkg('node', 'csslint'), CSS),
    ('mirrors-eslint', *lang_pkg('node', 'eslint'), JS),
    ('mirrors-fixmyjs', *lang_pkg('node', 'fixmyjs'), JS),
    ('mirrors-isort', *lang_pkg('python', 'isort'), PY),
    ('mirrors-jshint', *lang_pkg('node', 'jshint'), JS),
    (
        'mirrors-mypy',
        *lang_pkg('python', 'mypy'), PY, '--args=--ignore-missing-imports',
    ),
    ('mirrors-puppet-lint', *lang_pkg('ruby', 'puppet-lint'), PP),
    ('mirrors-pylint', *lang_pkg('python', 'pylint'), PY),
    ('mirrors-ruby-lint', *lang_pkg('ruby', 'ruby-lint'), RB),
    (
        'mirrors-scss-lint',
        *lang_pkg('ruby', 'scss_lint'), SCSS, '--entry=scss-lint',
    ),
    ('mirrors-yapf', *lang_pkg('python', 'yapf'), PY, '--args=-i'),
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    token = os.environ['GH_TOKEN']
    os.environ['GIT_AUTHOR_NAME'] = 'pre-commit'
    os.environ['GIT_AUTHOR_EMAIL'] = 'pre-commit@example.com'
    os.environ['GIT_COMMITTER_NAME'] = 'pre-commit'
    os.environ['GIT_COMMITTER_EMAIL'] = 'pre-commit@example.com'

    with tempfile.TemporaryDirectory() as tmpdir:
        for repo in REPOS:
            repo_name, *cmd_args = repo
            repodir = os.path.join(tmpdir, repo_name)
            subprocess.check_call((
                'git', 'clone',
                f'https://{token}@github.com/pre-commit/{repo_name}', repodir,
            ))
            subprocess.check_call((
                sys.executable, '-m', 'pre_commit_mirror_maker.main',
                repodir, *cmd_args,
            ))
            if not args.dry_run:
                subprocess.check_call((
                    'git', '-C', repodir, 'push', 'origin', 'HEAD', '--tags',
                ))
            else:
                print('Skipping push due to dry run...')
    return 0


if __name__ == '__main__':
    exit(main())
