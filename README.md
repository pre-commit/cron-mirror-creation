# DEPRECATED

This repository has been replaced with github actions on each of the mirror
repositories.  Here is [an example].

[an example]: https://github.com/pre-commit/mirrors-autopep8/blob/master/.github/workflows/main.yml
___

[![Build Status](https://travis-ci.org/pre-commit/cron-mirror-creation.svg?branch=master)](https://travis-ci.org/pre-commit/cron-mirror-creation)

cron-mirror-creation
====================

Periodically update pre-commit mirror repositories.

This was written to solve [this issue][1].

Currently it is cronned daily using [travis ci cron][2].

[1]: https://github.com/pre-commit/pre-commit/issues/265
[2]: https://docs.travis-ci.com/user/cron-jobs/
