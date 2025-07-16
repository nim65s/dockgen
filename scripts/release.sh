#!/bin/bash -eux
# ./docs/release.sh {major, minor, patch}

[[ $(basename "$PWD") == docs ]] && cd ..


OLD=$(uv version --short)
uv version --bump $1
NEW=$(uv version --short)
DATE=$(date +%Y-%m-%d)

sed -i "/^version =/s/$OLD/$NEW/" pyproject.toml
sed -i "/^## \[Unreleased\]/a \\\n## [v$NEW] - $DATE" CHANGELOG.md
sed -i "/^\[Unreleased\]/s/$OLD/$NEW/" CHANGELOG.md
sed -i "/^\[Unreleased\]/a [v$NEW]: https://github.com/nim65s/dockgen/compare/v$OLD...v$NEW" CHANGELOG.md

git add pyproject.toml uv.lock CHANGELOG.md
git commit -m "Release v$NEW"
git tag -s "v$NEW" -m "Release v$NEW"
git push
git push --tags
