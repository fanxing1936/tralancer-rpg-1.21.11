# 清除篡夺者战的全部实体。模型部件随载体一起清掉；圣坛的屏障方块先拆。
function rpg:usurper_boss/altar_clear
tag @e[tag=rpg.unit] remove rpg.usb.shit
tag @e[tag=rpg.unit] remove rpg.usb.dhit
tag @e[tag=rpg.unit] remove rpg.usb.hit
tag @e[tag=rpg.unit] remove rpg.usb.safe
execute as @e[type=minecraft:vindicator,tag=rpg.usb] run function rpg:usurper_boss/clear_unit
kill @e[type=minecraft:marker,tag=rpg.usb.center]
kill @e[tag=rpg.usb.fx]
execute as @e[tag=rpg.usb.unit] run function rpg:usurper_boss/clear_unit
execute as @e[tag=rpg.unit,tag=rpg.usb.rw] run function rpg:usurper_boss/rewrite/clear
bossbar set rpg:usurper_boss visible false
bossbar set rpg:usurper_boss players
stopsound @a record rpg:bgm.usurper1
stopsound @a record rpg:bgm.usurper2
scoreboard players set #fight rpg_ub 0
scoreboard players set #stage rpg_ub 0
