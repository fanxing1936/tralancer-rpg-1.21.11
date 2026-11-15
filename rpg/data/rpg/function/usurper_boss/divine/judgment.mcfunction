# 新约技能打到篡夺者：固定 100，二阶段 125（玩家承受的是力，克制他偷来的权）；不走百分比和斩杀线
tag @s add rpg.divine.hit
# 神圣之光无视无敌：他无敌的时候（变身、超载、天降半空、倒地）不吃
execute if data entity @s {Invulnerable:1b} run return 0
scoreboard players set @s rpg_lt_max 10000
execute if score #stage rpg_ub matches 2 run scoreboard players set @s rpg_lt_max 12500
function rpg:divine/damage/apply_score
particle minecraft:enchanted_hit ~ ~1.5 ~ 0.5 1 0.5 0.1 16 normal
