# 同化满 100：堕入魔力
scoreboard players set @s rpg_force 2
tag @s add rpg.fallen
tag @s remove rpg.burnt
scoreboard players set @s rpg_assim 100
scoreboard players set @s rpg_taint 60
scoreboard players set @s rpg_fz_tp 60
scoreboard players set @s rpg_mana 0
attribute @s minecraft:max_health modifier remove rpg:vital
scoreboard players set @s rpg_fz_b 0
title @s times 10 70 20
title @s title {"text":"堕入魔力","color":"#A276BE","bold":true,"italic":false}
title @s subtitle {"text":"解掉所有契约、让魔化回到 0，就能回头","color":"#9C9A94","bold":false,"italic":false}
playsound minecraft:entity.wither.spawn player @s ~ ~ ~ 0.5 1.4
function rpg:force/refund_h
execute store result score @s rpg_q_fd run time query day
