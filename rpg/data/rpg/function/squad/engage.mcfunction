# 交战。目标没了就归队，够得着就砍，够不着就压上去。
execute unless score #mark rpg_squad matches 1 run function rpg:squad/stand_down
execute if entity @e[tag=rpg.sq.mark,distance=3.4..128] run function rpg:squad/walk_aim
execute if entity @e[tag=rpg.sq.mark,distance=..3.4] if entity @s[scores={rpg_sq_cd=..0}] run function rpg:squad/strike
