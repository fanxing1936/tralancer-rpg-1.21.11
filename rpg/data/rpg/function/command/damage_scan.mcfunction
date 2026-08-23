# Snapshot health for entities a player could plausibly have hit, and flag the
# ones whose health moved since last tick.  Run once per player from
# rpg:command/index instead of once per weapon-effect line for every entity.
#
# 一次遍历，逐实体进 damage_one 把三件事做完 —— 详见那边的注释。
execute as @e[type=!#rpg:no_damage_track,distance=..64] run function rpg:command/damage_one
