# Deterministic agitation curve. Escape has one trigger: rpg_agit reaching 100.
scoreboard players add @s rpg_seal_t 1
scoreboard players add @s rpg_rel_w 1
scoreboard players add @s rpg_rel_pulse 1
execute if score @s rpg_seal_t matches 200.. run scoreboard players add @s rpg_agit 1
execute if score @s rpg_seal_t matches 200.. run scoreboard players set @s rpg_seal_t 0
execute if score @s rpg_agit matches 101.. run scoreboard players set @s rpg_agit 100
function rpg:inquest/seal/warning_tick
execute if score @s rpg_agit matches 100.. run return run function rpg:inquest/seal/escape_gate
execute if score @s rpg_rel_pulse matches 200.. run scoreboard players set @s rpg_rel_pulse 0
execute if score @s rpg_rel_pulse matches 0 if score @s rpg_rel_cd matches ..0 if entity @s[tag=rpg.seal.active3] run function rpg:inquest/seal/ability/abaddon_scan
