# 碎甲抛飞（as 碎甲）：按序号往外、往下飞，最后落在地上
execute if score #c rpg_sl matches 2 if entity @s[tag=rpg.slb.shard.helmet] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^-0.25 ^0.35 ^-0.5
execute if score #c rpg_sl matches 4 if entity @s[tag=rpg.slb.shard.helmet] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^-0.25 ^0.15 ^-0.5
execute if score #c rpg_sl matches 6 if entity @s[tag=rpg.slb.shard.helmet] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^-0.25 ^-0.05 ^-0.45
execute if score #c rpg_sl matches 8 if entity @s[tag=rpg.slb.shard.helmet] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^-0.2 ^-0.25 ^-0.4
execute if score #c rpg_sl matches 10 if entity @s[tag=rpg.slb.shard.helmet] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^-0.2 ^-0.4 ^-0.35
execute if score #c rpg_sl matches 12 if entity @s[tag=rpg.slb.shard.helmet] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^-0.15 ^-0.5 ^-0.3
execute if score #c rpg_sl matches 14 if entity @s[tag=rpg.slb.shard.helmet] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^-0.1 ^-0.5 ^-0.2
execute if score #c rpg_sl matches 16 if entity @s[tag=rpg.slb.shard.helmet] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^-0.05 ^-0.3 ^-0.1
execute if score #c rpg_sl matches 2 if entity @s[tag=rpg.slb.shard.l_pauldron] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^0.5 ^0.25 ^-0.1
execute if score #c rpg_sl matches 4 if entity @s[tag=rpg.slb.shard.l_pauldron] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^0.5 ^0.1 ^-0.1
execute if score #c rpg_sl matches 6 if entity @s[tag=rpg.slb.shard.l_pauldron] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^0.45 ^-0.1 ^-0.1
execute if score #c rpg_sl matches 8 if entity @s[tag=rpg.slb.shard.l_pauldron] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^0.4 ^-0.25 ^-0.1
execute if score #c rpg_sl matches 10 if entity @s[tag=rpg.slb.shard.l_pauldron] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^0.3 ^-0.35 ^-0.05
execute if score #c rpg_sl matches 12 if entity @s[tag=rpg.slb.shard.l_pauldron] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^0.2 ^-0.4 ^0.0
execute if score #c rpg_sl matches 14 if entity @s[tag=rpg.slb.shard.l_pauldron] rotated as @e[type=minecraft:vindicator,tag=rpg.slb,tag=!rpg.slb.preview,limit=1] positioned as @s run tp @s ^0.1 ^-0.35 ^0.0
execute if score #c rpg_sl matches 2..14 at @s run tp @s ~ ~ ~ ~31 ~
execute if score #c rpg_sl matches 16 positioned ~ ~-0.2 ~ run particle minecraft:block{block_state:"minecraft:iron_block"} ~ ~ ~ 0.3 0.1 0.3 0 8
