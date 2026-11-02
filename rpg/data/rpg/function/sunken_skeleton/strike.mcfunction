# 有人进了距离：持弩的举弩放箭，其余的挥一下。冷却借用 rpg_sk 的个体分数。
scoreboard players set @s rpg_sk 40
execute if entity @s[type=minecraft:pillager] run return run function rpg:sunken_skeleton/anim/enter/shoot
function rpg:sunken_skeleton/anim/enter/attack
