# 影傀（as/at）：贴身打 5%
scoreboard players remove @s rpg_dt_life 1
execute if score @s rpg_dt_life matches ..0 run return run function rpg:daath_fight/minion/gone
execute positioned ~ ~2 ~ rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rpg.dt.pp,distance=..16] ~ ~ ~ ~ ~
particle minecraft:smoke ~ ~0.8 ~ 0.2 0.4 0.2 0.005 2
execute if score @s rpg_dt_gcd matches 1.. run return run scoreboard players remove @s rpg_dt_gcd 1
execute unless entity @a[tag=rpg.dt.in,distance=..1.8] run return 0
scoreboard players set @s rpg_dt_gcd 24
tag @p[tag=rpg.dt.in,distance=..1.8] add rpg.dt.hit
scoreboard players set #pc rpg_dt 5
execute as @e[type=minecraft:vindicator,tag=rpg.dtb,distance=..70,limit=1,sort=nearest] run tag @s add rpg.dt.it
function rpg:daath_fight/hurt/all
tag @e[type=minecraft:vindicator,tag=rpg.dtb] remove rpg.dt.it
playsound minecraft:entity.player.attack.sweep hostile @a[distance=..16] ~ ~ ~ 0.5 1.4
