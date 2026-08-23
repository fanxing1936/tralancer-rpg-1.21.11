# 你杀死了一个空缺者 —— 由 rpg:item/vac_kill 在击杀那一刻触发。
# 但空壳不会因为躯体死掉就消失：它跳到最近的人身上。
# 这正是驱魔存在的理由 —— 剑解决不了它。
advancement revoke @s only rpg:item/vac_kill
scoreboard players add @s rpg_taint 8
execute at @s run particle soul ~ ~1 ~ 0.5 0.6 0.5 0.08 40
execute at @s run playsound minecraft:entity.vex.death hostile @a[distance=..24] ~ ~ ~ 1 0.6
execute at @s if entity @e[type=minecraft:villager,tag=!rpg.vacant,distance=..16,limit=1] run function rpg:vacant/jump
execute at @s unless entity @e[type=minecraft:villager,tag=!rpg.vacant,distance=..16,limit=1] run function rpg:vacant/loose
