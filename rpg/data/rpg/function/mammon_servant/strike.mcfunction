# 有人进了距离：持弩的与司祭远程出手，其余的近战。冷却借用 rpg_mms 的个体分数。
scoreboard players set @s rpg_mms 50
execute if entity @s[type=minecraft:pillager] run return run function rpg:mammon_servant/anim/enter/shoot
execute if entity @s[type=minecraft:evoker] run return run function rpg:mammon_servant/anim/enter/shoot
function rpg:mammon_servant/anim/enter/attack
