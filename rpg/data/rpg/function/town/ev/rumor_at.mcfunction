scoreboard players operation #t rpg_tl = @s rpg_tw_id
execute as @a[distance=..120,gamemode=!spectator,limit=1,sort=random] at @s as @e[type=minecraft:villager,tag=rpg.tnpc.folk,distance=..16,limit=1,sort=nearest] at @s run function rpg:town/ev/rumor_one
