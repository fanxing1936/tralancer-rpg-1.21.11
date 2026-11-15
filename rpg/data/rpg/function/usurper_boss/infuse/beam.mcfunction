# 光束（as 被灌注的罪仆，at 他胸前并朝向它）：量出距离，拉长到那里
scoreboard players set #d rpg_ub 0
function rpg:usurper_boss/infuse/step
execute as @e[tag=rpg.usb.ibeam,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[tag=rpg.usb.ibeam,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:2}
execute as @e[tag=rpg.usb.ibeam,limit=1] store result entity @s transformation.scale[2] float 1 run scoreboard players get #d rpg_ub
execute as @e[tag=rpg.usb.ibeam,limit=1] store result entity @s transformation.translation[2] float 0.5 run scoreboard players get #d rpg_ub
