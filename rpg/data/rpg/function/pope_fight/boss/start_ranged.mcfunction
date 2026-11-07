# 远程四拍轮换：扇形、天罚、扇形、圣环。
scoreboard players set #pb rpg_pf 0
scoreboard players add #ps rpg_pf 1
execute if score #ps rpg_pf matches 4.. run scoreboard players set #ps rpg_pf 0
execute if score #ps rpg_pf matches 1 run return run function rpg:pope_fight/boss/start_judge
execute if score #ps rpg_pf matches 3 run return run function rpg:pope_fight/boss/start_ring
function rpg:pope_fight/boss/start_attack
