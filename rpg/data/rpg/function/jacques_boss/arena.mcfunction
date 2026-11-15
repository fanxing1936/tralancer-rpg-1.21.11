# 战场（as/at 战场中心）。
scoreboard players add #tick rpg_jq 1
execute if entity @e[tag=rpg.unit.f,distance=..40] run scoreboard players set #empty rpg_jq 0
execute unless entity @e[tag=rpg.unit.f,distance=..40] run scoreboard players add #empty rpg_jq 1
execute if score #empty rpg_jq matches 1200.. run return run function rpg:jacques_boss/lose
execute unless entity @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,distance=..120] run return run function rpg:jacques_boss/lost_unit
bossbar set rpg:jacques_boss players @a[distance=..48]
execute as @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,distance=..120] at @s run function rpg:jacques_boss/unit
execute as @e[tag=rpg.jqb.fx,distance=..120] at @s run function rpg:jacques_boss/fx/tick
execute as @e[type=minecraft:vindicator,tag=rpg.jqd,distance=..120] at @s run function rpg:jacques_boss/david/tick
execute as @e[tag=rpg.unit,tag=rpg.jqb.cursed] at @s run function rpg:jacques_boss/curse/tick
function rpg:jacques_boss/music/tick
