scoreboard players add @s rpg_dt_t 1
execute facing entity @p[tag=rpg.dt.me] feet rotated ~ 0 run rotate @s ~ ~
execute unless entity @a[tag=rpg.dt.me,distance=..2.4] if score @s rpg_dt_t matches 30.. at @s run tp @s ^ ^ ^0.05
scoreboard players operation #m rpg_dt = @s rpg_dt_t
scoreboard players set #k rpg_dt 26
scoreboard players operation #m rpg_dt %= #k rpg_dt
execute if score #m rpg_dt matches 0 as @a[tag=rpg.dt.me,limit=1] at @s run playsound minecraft:entity.warden.heartbeat record @s ~ ~ ~ 1 0.7
execute at @a[tag=rpg.dt.me,limit=1] run particle minecraft:smoke ~ ~0.3 ~ 0.4 0.25 0.4 0.005 3
execute if score #m rpg_dt matches 0 run particle minecraft:end_rod ~ ~1.1 ~ 0.4 0.8 0.4 0.005 3
title @a[tag=rpg.dt.me,limit=1] actionbar ["",{"text":"它在等你走过去。潜行，站在它面前。","color":"#AAB4C3","bold":false,"italic":false}]
execute if score @s rpg_dt_t matches 70 run tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"selector":"@a[tag=rpg.dt.me,limit=1]","color":"#FFFFFF","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"那些事，是谁做的？","color":"#E6DFCF","bold":false,"italic":false},{"text":"　All of that. Who did it?","color":"#8F7430","bold":false,"italic":true}]
execute if score @s rpg_dt_t matches 70 run execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s17 voice @s ~ ~ ~ 1 1 1
execute if score @s rpg_dt_t matches 130 run tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"selector":"@a[tag=rpg.dt.me,limit=1]","color":"#FFFFFF","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"不是我。是你。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　Not I. You.","color":"#8F7430","bold":false,"italic":true}]
execute if score @s rpg_dt_t matches 130 run execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s18 voice @s ~ ~ ~ 1 1 1
execute unless entity @a[tag=rpg.dt.me,distance=..2.8,predicate=rpg:sneaking] run scoreboard players set @s rpg_dt_i 0
execute if entity @a[tag=rpg.dt.me,distance=..2.8,predicate=rpg:sneaking] run scoreboard players add @s rpg_dt_i 1
execute if score @s rpg_dt_i matches 40.. run return run function rpg:daath_fight/despair/met
execute if score @s rpg_dt_t matches 240.. run function rpg:daath_fight/despair/missed
