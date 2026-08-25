# @s 是刚拿到第 4 槽的 Boss。骑乘 marker 是它的死亡探针：
# 区块卸载时两者一起卸载，槽位保留；Boss 死亡时 marker 被甩下，释放槽位。
scoreboard players set @s rpg_boss_slot 4
summon minecraft:marker ~ ~ ~ {Tags:["rpg.bossbar.probe","rpg.bossbar.new"]}
scoreboard players set @e[type=minecraft:marker,tag=rpg.bossbar.new,distance=..1,limit=1,sort=nearest] rpg_boss_slot 4
ride @e[type=minecraft:marker,tag=rpg.bossbar.new,distance=..1,limit=1,sort=nearest] mount @s
tag @e[type=minecraft:marker,tag=rpg.bossbar.new,distance=..1] remove rpg.bossbar.new
scoreboard players set #boss_slot4 rpg_boss_slot 1
