# 末影面容：目标周围升起三张。
execute at @a[tag=rpg.pf.tgt,limit=1] rotated ~0 0 positioned ^ ^ ^7 positioned over motion_blocking_no_leaves facing entity @a[tag=rpg.pf.tgt,limit=1] feet rotated ~ 0 run function rpg:pope_fight/heart/face_gaze
execute at @a[tag=rpg.pf.tgt,limit=1] rotated ~120 0 positioned ^ ^ ^7 positioned over motion_blocking_no_leaves facing entity @a[tag=rpg.pf.tgt,limit=1] feet rotated ~ 0 run function rpg:pope_fight/heart/face_gaze
execute at @a[tag=rpg.pf.tgt,limit=1] rotated ~240 0 positioned ^ ^ ^7 positioned over motion_blocking_no_leaves facing entity @a[tag=rpg.pf.tgt,limit=1] feet rotated ~ 0 run function rpg:pope_fight/heart/face_gaze
playsound rpg:heart_of_ender.mortar_explode hostile @a[distance=..32] ~ ~ ~ 0.5 0.6
