# 第 5 段（萨麦尔）亮起：符文换亮色、放大，预警 0.6 秒
execute as @e[tag=rpg.usb.rs4] run data modify entity @s text.color set value "#FF5C52"
execute as @e[tag=rpg.usb.rs4] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{scale:[3.125f,3.125f,3.125f]}}
execute rotated 141.4 0 positioned ^ ^ ^10 run function rpg:usurper_boss/ring/warn4
playsound rpg:usurper.chime hostile @a[distance=..32] ~ ~ ~ 1 1.10
