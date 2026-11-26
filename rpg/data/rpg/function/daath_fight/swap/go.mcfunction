# 互换位置；你原来的地方留下一记影爆
summon minecraft:marker ~ ~ ~ {Tags:["rpg.dt.fx","rpg.dt.sw1"]}
scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.sw1,distance=..1] rpg_dt_life 60
scoreboard players set @e[type=minecraft:marker,tag=rpg.dt.sw1,distance=..1] rpg_dt_kd 0
execute at @a[tag=rpg.dt.me,limit=1] run tp @s ~ ~ ~
execute at @e[type=minecraft:marker,tag=rpg.dt.sw1,distance=..60,limit=1] run tp @a[tag=rpg.dt.me,limit=1] ~ ~ ~
execute at @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/swap/mark
playsound minecraft:entity.enderman.teleport hostile @a[distance=..48] ~ ~ ~ 1 0.6
execute at @a[tag=rpg.dt.me,limit=1] run playsound minecraft:block.glass.break hostile @a[tag=rpg.dt.me,limit=1] ~ ~ ~ 0.8 1.4
