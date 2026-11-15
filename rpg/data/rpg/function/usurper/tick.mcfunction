# 篡夺者每刻入口。任何召唤路径落地的第 0 柱都在这里换装（含封印逃逸、调试召唤）。
execute if entity @e[type=minecraft:vindicator,tag=rpg.usb,tag=!rpg.usb.s2,tag=!rpg.usm,limit=1] as @e[type=minecraft:vindicator,tag=rpg.usb,tag=!rpg.usb.s2,tag=!rpg.usm] at @s run function rpg:usurper/dress
execute if entity @e[type=minecraft:vindicator,tag=rpg.usm,limit=1] as @e[type=minecraft:vindicator,tag=rpg.usm] at @s run function rpg:usurper/follow
execute if entity @e[type=minecraft:item_display,tag=rpg.usm.part,predicate=!rpg:usurper/riding,limit=1] run function rpg:usurper/orphans
