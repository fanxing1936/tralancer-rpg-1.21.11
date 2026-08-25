
# @s=当前二阶段 Boss，执行位置=Boss。逐位玩家生成独立爆心，击杀归 Boss。
tag @e[tag=rpg.pseudo_boom.source] remove rpg.pseudo_boom.source
tag @s add rpg.pseudo_boom.source
execute as @a[distance=..10,gamemode=!spectator,gamemode=!creative] at @s run function rpg:effect/pseudo_explosion/sourced_p3
tag @s remove rpg.pseudo_boom.source
