# 奖品原样落下来，归开箱人；宝库解锁
tag @s add rpg.vt.me_c
execute as @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6] run function rpg:vault/drop
kill @e[type=minecraft:item_display,tag=rpg.vt.me,distance=..6]
execute as @e[type=minecraft:text_display,tag=rpg.vt.t,distance=..5] if score @s rpg_vt_id = #c rpg_vt run kill @s
playsound minecraft:block.vault.close_shutter block @a[distance=..16] ~ ~ ~ 1 1
execute if score @s rpg_vt_m matches 0 positioned ~ ~-1.55 ~ if block ~ ~ ~ minecraft:vault run function rpg:vault/unlock_0
execute if score @s rpg_vt_m matches 1 positioned ~ ~-1.55 ~ if block ~ ~ ~ minecraft:vault run function rpg:vault/unlock_1
kill @s
