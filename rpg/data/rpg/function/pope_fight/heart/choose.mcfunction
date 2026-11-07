# 大招优先；目标跑远就潜地追上；否则六招轮换，破绽落在固定的位置上。
execute if score #ultq rpg_pf matches 1 run return run function rpg:pope_fight/heart/start_ult
execute if score #ultcd rpg_pf matches 0 run return run function rpg:pope_fight/heart/start_ult
execute unless entity @a[tag=rpg.pf.tgt,limit=1,distance=..20] run return run function rpg:pope_fight/heart/start_sink
scoreboard players add #seq rpg_pf 1
execute if score #seq rpg_pf matches 6.. run scoreboard players set #seq rpg_pf 0
execute if score #seq rpg_pf matches 1 run return run function rpg:pope_fight/heart/start_mortar
execute if score #seq rpg_pf matches 2 run return run function rpg:pope_fight/heart/start_vent
execute if score #seq rpg_pf matches 3 run return run function rpg:pope_fight/heart/start_cross
execute if score #seq rpg_pf matches 4 run return run function rpg:pope_fight/heart/start_gaze
execute if score #seq rpg_pf matches 5 run return run function rpg:pope_fight/heart/start_nova
function rpg:pope_fight/heart/start_sink
