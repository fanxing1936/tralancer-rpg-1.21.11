# 破绽：权柄没有执行者，伤害加一半（至少留 1 血，交给切段判定）
scoreboard players operation #hp rpg_ub -= #lost rpg_ub
execute if score #hp rpg_ub matches ..10 run scoreboard players set #hp rpg_ub 10
execute store result entity @s Health float 0.1 run scoreboard players get #hp rpg_ub
