# 毁约。恩赐与枷锁一同撤走，柱位清空。
attribute @s minecraft:movement_speed modifier remove rpg:pact/2/boon0
attribute @s minecraft:max_health modifier remove rpg:pact/2/bane0
scoreboard players set @s rpg_pact 0
scoreboard players set @s rpg_pact_cd 0
tag @s remove rpg.pact
playsound minecraft:block.glass.break master @s ~ ~ ~ 1 0.5
