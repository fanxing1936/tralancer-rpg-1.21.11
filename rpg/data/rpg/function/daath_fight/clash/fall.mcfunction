tag @s remove rpg.dt.window
tag @s remove rpg.dt.clash
execute at @a[tag=rpg.dt.me,limit=1] rotated ~ 0 run tp @s ^ ^ ^1.8
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute positioned ~ ~ ~ run tag @a[distance=..6,tag=rpg.dt.me,gamemode=!spectator,gamemode=!creative] add rpg.dt.hit
execute if entity @a[tag=rpg.dt.hit] run scoreboard players set #pc rpg_dt 24
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/hurt/all
execute at @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/clash/boom
