# 战场（as/at 战场中心）。
scoreboard players add #tick rpg_lub 1
execute if entity @e[tag=rpg.unit.f,distance=..40] run scoreboard players set #empty rpg_lub 0
execute unless entity @e[tag=rpg.unit.f,distance=..40] run scoreboard players add #empty rpg_lub 1
execute if score #empty rpg_lub matches 1200.. run return run function rpg:lucifer_boss/lose
execute unless entity @e[type=minecraft:vindicator,tag=rpg.lub,distance=..120] run return run function rpg:lucifer_boss/lost_unit
bossbar set rpg:lucifer_boss players @a[distance=..48]
execute as @e[type=minecraft:vindicator,tag=rpg.lub,distance=..120] at @s run function rpg:lucifer_boss/unit
function rpg:lucifer_boss/music/tick
