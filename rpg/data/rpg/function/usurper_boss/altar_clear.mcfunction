# 圣坛的屏障方块（任何结束路径都要先拆，再清实体）
execute at @e[type=minecraft:marker,tag=rpg.usb.altar] run fill ~ ~ ~ ~1 ~1 ~1 minecraft:air replace minecraft:barrier
kill @e[type=minecraft:marker,tag=rpg.usb.altar]
