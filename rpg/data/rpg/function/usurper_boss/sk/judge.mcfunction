execute if score @s rpg_ub_t matches 20 run function rpg:usurper_boss/judge/pose
execute if score @s rpg_ub_t matches 16 run function rpg:usurper_boss/judge/tele0
execute if score @s rpg_ub_t matches 30 run function rpg:usurper_boss/judge/fire0
execute if score @s rpg_ub_t matches 38 run execute as @e[tag=rpg.usb.jb0] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0.01f,0.01f,20f]}}
execute if score @s rpg_ub_t matches 26 run function rpg:usurper_boss/judge/tele1
execute if score @s rpg_ub_t matches 40 run function rpg:usurper_boss/judge/fire1
execute if score @s rpg_ub_t matches 48 run execute as @e[tag=rpg.usb.jb1] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0.01f,0.01f,20f]}}
execute if score @s rpg_ub_t matches 36 run function rpg:usurper_boss/judge/tele2
execute if score @s rpg_ub_t matches 50 run function rpg:usurper_boss/judge/fire2
execute if score @s rpg_ub_t matches 58 run execute as @e[tag=rpg.usb.jb2] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0.01f,0.01f,20f]}}
execute if score @s rpg_ub_t matches 46 run function rpg:usurper_boss/judge/tele3
execute if score @s rpg_ub_t matches 60 run function rpg:usurper_boss/judge/fire3
execute if score @s rpg_ub_t matches 68 run execute as @e[tag=rpg.usb.jb3] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0.01f,0.01f,20f]}}
execute if score @s rpg_ub_t matches 56 run function rpg:usurper_boss/judge/tele4
execute if score @s rpg_ub_t matches 70 run function rpg:usurper_boss/judge/fire4
execute if score @s rpg_ub_t matches 78 run execute as @e[tag=rpg.usb.jb4] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0.01f,0.01f,20f]}}
execute if score @s rpg_ub_t matches 86 run function rpg:usurper_boss/weak/ult
execute if score @s rpg_ub_t matches 90.. run function rpg:usurper_boss/sk/end
