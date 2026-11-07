# 全场圣印，加三处圣所；随机转一个角度。
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/doom_seal
execute store result score #r rpg_pf run random value 0..3
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] if score #r rpg_pf matches 0 rotated 0 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/refuge
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] if score #r rpg_pf matches 0 rotated 120 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/refuge
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] if score #r rpg_pf matches 0 rotated 240 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/refuge
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] if score #r rpg_pf matches 1 rotated 30 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/refuge
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] if score #r rpg_pf matches 1 rotated 150 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/refuge
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] if score #r rpg_pf matches 1 rotated 270 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/refuge
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] if score #r rpg_pf matches 2 rotated 60 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/refuge
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] if score #r rpg_pf matches 2 rotated 180 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/refuge
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] if score #r rpg_pf matches 2 rotated 300 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/refuge
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] if score #r rpg_pf matches 3 rotated 90 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/refuge
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] if score #r rpg_pf matches 3 rotated 210 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/refuge
execute at @e[type=minecraft:marker,tag=rpg.pf.center,limit=1] if score #r rpg_pf matches 3 rotated 330 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves run function rpg:pope_fight/fx/refuge
