# 一圈面容，朝向圈心，张嘴后一起转。
execute at @a[tag=rpg.pf.tgt,limit=1] rotated 30 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves rotated ~180 0 run function rpg:pope_fight/heart/face_ccw
execute at @a[tag=rpg.pf.tgt,limit=1] rotated 90 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves rotated ~180 0 run function rpg:pope_fight/heart/face_ccw
execute at @a[tag=rpg.pf.tgt,limit=1] rotated 150 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves rotated ~180 0 run function rpg:pope_fight/heart/face_ccw
execute at @a[tag=rpg.pf.tgt,limit=1] rotated 210 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves rotated ~180 0 run function rpg:pope_fight/heart/face_ccw
execute at @a[tag=rpg.pf.tgt,limit=1] rotated 270 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves rotated ~180 0 run function rpg:pope_fight/heart/face_ccw
execute at @a[tag=rpg.pf.tgt,limit=1] rotated 330 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves rotated ~180 0 run function rpg:pope_fight/heart/face_ccw
playsound rpg:heart_of_ender.mortar_explode hostile @a[distance=..48] ~ ~ ~ 0.7 0.6
