# 第 6 段（贝利尔）亮起：符文换亮色、放大，预警 0.6 秒
execute as @e[tag=rpg.usb.rs5] run data modify entity @s text.color set value "#D97AD9"
execute as @e[tag=rpg.usb.rs5] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{scale:[3.125f,3.125f,3.125f]}}
execute rotated 192.9 0 positioned ^ ^ ^10 run function rpg:usurper_boss/ring/warn5
playsound rpg:usurper.chime hostile @a[distance=..32] ~ ~ ~ 1 1.20
