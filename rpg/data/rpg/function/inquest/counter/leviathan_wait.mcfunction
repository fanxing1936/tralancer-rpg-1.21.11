scoreboard players set #clone_found rpg_ex_tmp 0
tag @s add rpg.rite.anchor.active
execute as @e[type=minecraft:husk,tag=rpg.counter.clone,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:item_display,tag=rpg.rite.anchor.active,limit=1] rpg_rite_id run scoreboard players set #clone_found rpg_ex_tmp 1
tag @s remove rpg.rite.anchor.active
execute if score #clone_found rpg_ex_tmp matches 0 run return run function rpg:inquest/counter/leviathan_win
scoreboard players remove @s rpg_ex_ctime 1
execute if score @s rpg_ex_ctime matches ..0 run function rpg:inquest/counter/leviathan_timeout
