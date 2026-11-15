# 战场（as/at 战场中心）。
scoreboard players add #tick rpg_ub 1
execute if entity @e[tag=rpg.unit.f,distance=..40] run scoreboard players set #empty rpg_ub 0
execute unless entity @e[tag=rpg.unit.f,distance=..40] run scoreboard players add #empty rpg_ub 1
execute if score #empty rpg_ub matches 1200.. run return run function rpg:usurper_boss/lose
execute unless entity @e[type=minecraft:vindicator,tag=rpg.usb,distance=..120] run return run function rpg:usurper_boss/lost_unit
bossbar set rpg:usurper_boss players @a[distance=..48]
execute as @e[type=minecraft:vindicator,tag=rpg.usb,distance=..120] at @s run function rpg:usurper_boss/unit
function rpg:usurper_boss/music/tick
execute as @e[tag=rpg.usb.fx,distance=..120] at @s run function rpg:usurper_boss/fx/tick
execute as @e[tag=rpg.unit,tag=rpg.usb.rw] run function rpg:usurper_boss/rewrite/tick
