# 宝库：钥匙开出触发星，这里接手（add_vault.py）
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger2] at @s align xyz positioned ~0.5 ~-1 ~0.5 run function rpg:vault/open
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s align xyz positioned ~0.5 ~-1 ~0.5 run function rpg:vault/open_om
execute as @e[type=minecraft:marker,tag=rpg.vt.c] at @s run function rpg:vault/step
