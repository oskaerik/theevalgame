#!/bin/bash

set -eo pipefail

rm -rf dist ../oskaerik.github.io/theevalgame/

pipenv run flet publish main.py --base-url theevalgame --app-name "the eval game" --app-short-name theevalgame --app-description "A game testing your Python skills, inspired by The Password Game."

sed -i 's/<title>Flet<\/title>/<title>the eval game<\/title>/' dist/index.html

mv dist ../oskaerik.github.io/theevalgame
