# 圈画在 18 刻前你站的地方：走开就没事
execute at @e[type=minecraft:marker,tag=rpg.dt.bm,distance=..50,limit=1,sort=nearest] run tag @a[distance=..2.2,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute as @a[tag=rpg.dt.hit] run effect give @s minecraft:slowness 2 9 true
execute as @a[tag=rpg.dt.hit] at @s run function rpg:daath_fight/bind/fx
execute if entity @a[tag=rpg.dt.hit] run scoreboard players set #pc rpg_dt 7
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/hurt/all
