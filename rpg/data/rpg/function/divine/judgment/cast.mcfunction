scoreboard players set @s rpg_lt_judge 0
tag @s add rpg.divine.cast
execute as @e[tag=rpg.divine.judgment.target,distance=..8,sort=nearest,limit=1] at @s run function rpg:divine/judgment/strike
tag @s remove rpg.divine.cast
playsound minecraft:entity.lightning_bolt.impact player @s ~ ~ ~ 0.75 1.75
function rpg:hud/m65
