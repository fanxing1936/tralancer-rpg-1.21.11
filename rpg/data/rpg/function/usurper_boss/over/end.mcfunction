# 收势（as 载体）：圣坛撤下，他落地，4 秒破绽
function rpg:usurper_boss/altar_clear
kill @e[tag=rpg.usb.overv]
execute at @e[type=minecraft:marker,tag=rpg.usb.center,limit=1] run tp @s ~ ~ ~
data merge entity @s {Invulnerable:0b,NoGravity:0b}
function rpg:usurper_boss/weak/ult
execute at @s run function rpg:usurper_boss/over/land
