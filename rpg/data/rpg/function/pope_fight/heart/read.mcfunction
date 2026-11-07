# 每 5 刻读一次血量（一次 NBT），外壳把这段时间的伤害退回七成；再选目标。
scoreboard players set #h rpg_pf 0
execute store result score #hp rpg_pf run data get entity @s Health
scoreboard players operation #lost rpg_pf = #last rpg_pf
scoreboard players operation #lost rpg_pf -= #hp rpg_pf
execute if score #lost rpg_pf matches 1.. run function rpg:pope_fight/heart/hurt
scoreboard players operation #last rpg_pf = #hp rpg_pf
execute store result bossbar minecraft:pope value run scoreboard players get #hp rpg_pf
function rpg:pope_fight/bar/hp
execute if score #hp rpg_pf matches ..5 run return run function rpg:pope_fight/heart/die
execute if score #ultl rpg_pf matches 750 if score #hp rpg_pf matches ..750 run function rpg:pope_fight/heart/ult_due
execute if score #ultl rpg_pf matches 500 if score #hp rpg_pf matches ..500 run function rpg:pope_fight/heart/ult_due
execute if score #ultl rpg_pf matches 250 if score #hp rpg_pf matches ..250 run function rpg:pope_fight/heart/ult_due
tag @a[tag=rpg.pf.tgt] remove rpg.pf.tgt
tag @a[distance=..48,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] add rpg.pf.tgt
