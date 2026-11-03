# 有人进了距离：持弩的与司祭举臂施法，其余的双爪下劈。冷却借用 rpg_tw 的个体分数。
scoreboard players set @s rpg_tw 50
execute if entity @s[type=minecraft:pillager] run return run function rpg:tower_wraith/anim/enter/cast
execute if entity @s[type=minecraft:evoker] run return run function rpg:tower_wraith/anim/enter/cast
function rpg:tower_wraith/anim/enter/attack
