scoreboard players set #bound_found rpg_ex_tmp 0
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:vindicator,tag=rpg.exorcism.bound,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run scoreboard players set #bound_found rpg_ex_tmp 1
execute if score #bound_found rpg_ex_tmp matches 0 run return run function rpg:inquest/anchor_orphan
scoreboard players remove @s rpg_totem 1
execute if score @s rpg_totem matches ..0 run return run function rpg:inquest/anchor_timeout
execute if score @s rpg_ex_toolcd matches 1.. run scoreboard players remove @s rpg_ex_toolcd 1
function rpg:inquest/stability/show
particle dust{color:[1.0,0.91,0.52],scale:0.7} ~ ~0.75 ~ 0.28 0.35 0.28 0.01 1 normal
execute if score @s rpg_ex_stage matches 2 run function rpg:inquest/tool/scan
execute if score @s rpg_ex_stage matches 2 if score @s rpg_ex_phase matches 1.. run function rpg:inquest/phase2/tick
execute if score @s rpg_ex_stage matches 2 if score @s rpg_ex_phase matches ..0 run function rpg:inquest/phase2/pressure_tick
execute if score @s rpg_ex_stage matches 2 if score @s rpg_ex_wave matches 1.. run function rpg:inquest/phase2/wave_tick
execute if score @s rpg_ex_stage matches 2 if score @s rpg_ex_phase matches ..0 run function rpg:inquest/counter/tick
execute if score @s rpg_ex_stage matches 2 if score @s rpg_ex_phase matches ..0 run function rpg:inquest/struggle_tick
execute if score @s rpg_ex_stab matches ..0 run return run function rpg:inquest/anchor_collapse
execute if score @s rpg_ex_stage matches 2 if score @s rpg_ex_stab matches 100.. run return run function rpg:inquest/start_verdict
execute if score @s rpg_ex_ransom matches 1.. run return run function rpg:inquest/counter/mammon_wait
execute if score @s rpg_ex_stage matches 2 run return run function rpg:inquest/anchor_stage2
execute if score @s rpg_ex_stage matches 4 run return run function rpg:inquest/anchor_stage4
tag @s remove rpg.rite.anchor.active
