# 新约技能打到末影之心：固定 100，没有斩杀线；外壳照常吃掉七成。
scoreboard players set @s rpg_lt_max 10000
function rpg:divine/damage/apply_score
particle minecraft:enchanted_hit ~ ~3 ~ 0.8 1.5 0.8 0.1 16 normal
