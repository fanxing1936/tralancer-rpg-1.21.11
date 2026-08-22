#!/bin/sh
# Rebuild the upgraded pack from the pristine 1.21 copy in _orig/.
set -e
cd "$(dirname "$0")"
rm -rf ../rpg
cp -r ../_orig ../rpg
echo "== 1. version migration 1.21 -> 1.21.11 =="
python migrate.py   ../rpg
echo
echo "== 2. tick-path optimisation =="
python optimize.py  ../rpg
python opt_spawn.py ../rpg
python opt_misc.py  ../rpg
python add_items.py ../resourcepack ../rpg
python add_skills.py ../rpg
python add_twins.py  ../resourcepack ../rpg
python add_lucifer.py ../resourcepack ../rpg
python retype_longinus.py ../resourcepack ../rpg
python make_boxes.py ../rpg
echo
echo "== 2b. guard the empty-tag entity walks =="
python opt_index.py ../rpg
python opt_guard.py ../rpg
echo
echo "== 3. validation =="
python validate.py  ../rpg
echo
echo "== 4. per-tick profile =="
python profile_tick.py ../rpg
