# 毁约。恩赐与枷锁一同撤走，柱位清空。
# 这一柱不靠属性修饰符 —— 它的恩赐与枷锁都是逐刻的
scoreboard players set @s rpg_pact 0
scoreboard players set @s rpg_pact_cd 0
tag @s remove rpg.pact
playsound minecraft:block.glass.break master @s ~ ~ ~ 1 0.5
