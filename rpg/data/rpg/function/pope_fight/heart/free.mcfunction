function rpg:pope_fight/heart/steer
execute if score #cd rpg_pf matches 0 run return run function rpg:pope_fight/heart/choose
scoreboard players add #ba rpg_pf 1
execute if score #ba rpg_pf matches 30.. run return run function rpg:pope_fight/heart/basic
execute if entity @a[tag=rpg.pf.tgt,limit=1,distance=..4] run return run function rpg:pope_fight/heart/stop
execute unless entity @a[tag=rpg.pf.tgt,limit=1,distance=..6] run function rpg:pope_fight/heart/go
execute if score #walking rpg_pf matches 1 if score #bl rpg_pf matches 0 at @s positioned ^ ^ ^0.12 positioned over motion_blocking_no_leaves run function rpg:pope_fight/heart/place
