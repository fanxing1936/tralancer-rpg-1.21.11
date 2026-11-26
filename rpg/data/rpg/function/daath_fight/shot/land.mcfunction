tag @p[tag=rpg.dt.in,distance=..4] add rpg.dt.hit
scoreboard players operation #pc rpg_dt = @s rpg_dt_pc
execute as @e[type=minecraft:vindicator,tag=rpg.dtb,distance=..70,limit=1,sort=nearest] run tag @s add rpg.dt.it
function rpg:daath_fight/hurt/all
tag @e[type=minecraft:vindicator,tag=rpg.dtb] remove rpg.dt.it
particle minecraft:dust_color_transition{from_color:[0.85,0.87,0.91],to_color:[0.16,0.18,0.22],scale:1.1} ~ ~ ~ 0.2 0.2 0.2 0 8
playsound rpg:daath.impact hostile @a[distance=..24] ~ ~ ~ 1 1
kill @s
