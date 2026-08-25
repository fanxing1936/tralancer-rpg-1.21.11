scoreboard players add @s rpg_ex_stab 25
execute if score @s rpg_ex_stab matches 101.. run scoreboard players set @s rpg_ex_stab 100
execute at @s run particle dust{color:[0.38,0.85,0.91],scale:1.1} ~ ~0.18 ~ 0.8 0.08 0.8 0.04 28 force
execute at @s run particle minecraft:end_rod ~ ~0.25 ~ 0.7 0.12 0.7 0.03 18 force
execute at @s run playsound minecraft:block.amethyst_block.resonate master @a[distance=..24] ~ ~ ~ 0.75 1.55
execute at @s as @a[tag=rpg.divine.cast,distance=..24,sort=nearest,limit=1] run scoreboard players add @s rpg_ex_xp 4
