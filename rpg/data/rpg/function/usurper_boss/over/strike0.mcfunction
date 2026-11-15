# 第 1 波电光（as/at 载体）：圣坛顶上的人安全，其余人都挨
execute as @e[type=minecraft:marker,tag=rpg.usb.altar] at @s positioned ~0.1 ~1.95 ~0.1 run tag @e[tag=rpg.unit,dx=0.8,dy=0,dz=0.8] add rpg.usb.safe
execute as @e[tag=rpg.unit.f,distance=..40,tag=!rpg.usb.safe] at @s run function rpg:usurper_boss/over/zap
tag @e[tag=rpg.unit] remove rpg.usb.safe
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run function rpg:usurper_boss/over/sweep
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~7.0 ~ ~0.0 positioned over motion_blocking_no_leaves run function rpg:usurper_boss/over/bolt
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~6.0 ~ ~10.4 positioned over motion_blocking_no_leaves run function rpg:usurper_boss/over/bolt
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~-4.0 ~ ~6.9 positioned over motion_blocking_no_leaves run function rpg:usurper_boss/over/bolt
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~-13.0 ~ ~0.0 positioned over motion_blocking_no_leaves run function rpg:usurper_boss/over/bolt
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~-4.5 ~ ~-7.8 positioned over motion_blocking_no_leaves run function rpg:usurper_boss/over/bolt
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~7.0 ~ ~-12.1 positioned over motion_blocking_no_leaves run function rpg:usurper_boss/over/bolt
