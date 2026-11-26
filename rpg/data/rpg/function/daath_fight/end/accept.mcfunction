execute if score @s rpg_dt_t matches 6 run tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"selector":"@a[tag=rpg.dt.me,limit=1]","color":"#FFFFFF","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"我一直都在。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　I was always here.","color":"#8F7430","bold":false,"italic":true}]
execute if score @s rpg_dt_t matches 6 run execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s20 voice @s ~ ~ ~ 1 1 1
execute if score @s rpg_dt_t matches 6 run function rpg:daath/anim/enter/hero
execute if score @s rpg_dt_t matches 10..50 run execute facing entity @a[tag=rpg.dt.me,limit=1] feet rotated ~ 0 unless entity @a[tag=rpg.dt.me,distance=..0.6] run tp @s ^ ^ ^0.06 ~ ~
execute if score @s rpg_dt_t matches 10..60 run particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.02 3
execute if score @s rpg_dt_t matches 52 run function rpg:daath_fight/end/merge
execute if score @s rpg_dt_t matches 62 run function rpg:daath_fight/end/finish
