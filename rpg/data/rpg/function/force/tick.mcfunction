execute store result score #now rpg_fo run time query gametime
execute as @a[scores={rpg_fo_do=1..}] at @s run function rpg:force/press
execute as @a at @s run function rpg:force/fkey
execute as @a[scores={rpg_fo_buf=1..}] at @s run function rpg:force/buff/tick
execute as @a[scores={rpg_fo_mt=1..}] at @s run function rpg:force/sk/8/tick
execute as @e[tag=rpg.fo.mk] at @s run function rpg:force/sk/2/tick
execute as @e[type=minecraft:marker,tag=rpg.fo.zone] at @s run function rpg:force/zone/tick
execute as @e[tag=rpg.fo.hfx] at @s run function rpg:force/h/fx/tick
execute as @e[tag=rpg.fo.mfx] at @s run function rpg:force/m/fx/tick
execute as @a[scores={rpg_fo_d2=1..}] at @s run function rpg:force/x/id/dealt
execute as @a[scores={rpg_fo_tk=1..}] at @s run function rpg:force/x/l/saul_tick
execute as @a[scores={rpg_fo_wr=1..}] at @s run function rpg:force/x/f/wrath_tick
execute as @a[scores={rpg_fo_fl=1..}] at @s run function rpg:force/x/f/fall_tick
execute as @e[tag=rpg.fo.gd] at @s run function rpg:force/x/f/gild_tick
execute as @e[tag=rpg.fo.xh] at @s run function rpg:force/x/h/fx/tick
execute as @e[tag=rpg.fo.xm] at @s run function rpg:force/x/m/fx/tick
scoreboard players operation #m rpg_fo = #now rpg_fo
scoreboard players operation #m rpg_fo %= #20 rpg_fo
execute unless score #m rpg_fo matches 0 run return 0
execute as @e[tag=rpg.fo.timed] run function rpg:force/timed
execute as @a at @s run function rpg:force/sec
execute as @e[tag=rpg.fo.ch] at @s run function rpg:force/x/f/charm_sec
execute as @a[scores={rpg_fo_fe=1..}] at @s run function rpg:force/x/f/feast_sec
