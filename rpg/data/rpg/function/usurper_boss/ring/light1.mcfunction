# 第 2 段（利维坦）亮起：符文换亮色、放大，预警 0.6 秒
execute as @e[tag=rpg.usb.rs1] run data modify entity @s text.color set value "#4F9EF0"
execute as @e[tag=rpg.usb.rs1] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{scale:[3.125f,3.125f,3.125f]}}
execute rotated 347.1 0 positioned ^ ^ ^10 run function rpg:usurper_boss/ring/warn1
playsound rpg:usurper.chime hostile @a[distance=..32] ~ ~ ~ 1 0.80
