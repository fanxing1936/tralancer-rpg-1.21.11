# 第 2 波电光（as/at 载体）：圣坛顶上的人安全，其余人都挨
execute as @e[type=minecraft:marker,tag=rpg.usb.altar] at @s positioned ~0.1 ~1.95 ~0.1 run tag @e[tag=rpg.unit,dx=0.8,dy=0,dz=0.8] add rpg.usb.safe
execute as @e[tag=rpg.unit.f,distance=..40,tag=!rpg.usb.safe] at @s run function rpg:usurper_boss/over/zap
tag @e[tag=rpg.unit] remove rpg.usb.safe
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run function rpg:usurper_boss/over/sweep
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~8.0 ~ ~6.0 positioned over motion_blocking_no_leaves run function rpg:usurper_boss/over/bolt
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~-1.8 ~ ~14.9 positioned over motion_blocking_no_leaves run function rpg:usurper_boss/over/bolt
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~-10.1 ~ ~4.3 positioned over motion_blocking_no_leaves run function rpg:usurper_boss/over/bolt
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~-5.6 ~ ~-4.2 positioned over motion_blocking_no_leaves run function rpg:usurper_boss/over/bolt
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~1.5 ~ ~-11.9 positioned over motion_blocking_no_leaves run function rpg:usurper_boss/over/bolt
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] positioned ~7.4 ~ ~-3.1 positioned over motion_blocking_no_leaves run function rpg:usurper_boss/over/bolt
