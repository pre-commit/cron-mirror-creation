import argparse
import os.path
import subprocess
import sys
import tempfile


CSS = r'\.css$'
JS = r'\.js$'
PP = r'\.pp$'
PY = r'\.py$'
RB = r'\.rb$'
SCSS = r'\.scss$'

REPOS = (
    ('mirrors-autopep8', 'python', 'autopep8', PY, '--args=-i'),
    ('mirrors-coffeelint', 'node', 'coffeelint', r'\.(js|coffee)$'),
    ('mirrors-csslint', 'node', 'csslint', CSS),
    ('mirrors-eslint', 'node', 'eslint', JS),
    ('mirrors-fixmyjs', 'node', 'fixmyjs', JS),
    ('mirrors-jshint', 'node', 'jshint', JS),
    ('mirrors-puppet-lint', 'ruby', 'puppet-lint', PP),
    ('mirrors-pylint', 'python', 'pylint', PY),
    ('mirrors-ruby-lint', 'ruby', 'ruby-lint', RB),
    ('mirrors-scss-lint', 'ruby', 'scss_lint', SCSS, '--entry=scss-lint'),
    ('mirrors-yapf', 'python', 'yapf', PY, '--args=-i'),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    os.environ['GIT_AUTHOR_NAME'] = 'pre-commit'
    os.environ['GIT_AUTHOR_EMAIL'] = 'pre-commit@example.com'
    os.environ['GIT_COMMITTER_NAME'] = 'pre-commit'
    os.environ['GIT_COMMITTER_EMAIL'] = 'pre-commit@example.com'

    with tempfile.TemporaryDirectory() as tmpdir:
        for repo in REPOS:
            repo_name, *cmd_args = repo
            token = os.environ['GH_TOKEN']
            repodir = os.path.join(tmpdir, repo_name)
            subprocess.check_call((
                'git', 'clone',
                f'https://{token}@github.com/pre-commit/{repo_name}',
                repodir,
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


if __name__ == '__main__':
    exit(main())
