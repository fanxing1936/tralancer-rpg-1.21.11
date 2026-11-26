scoreboard players add @s rpg_dt_t 1
execute if score @s rpg_dt_t matches 20 run tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"text":"影","color":"#AAB4C3","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"我们如今对着镜子观看，模糊不清。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　Now we see through a glass, darkly.","color":"#8F7430","bold":false,"italic":true}]
execute if score @s rpg_dt_t matches 20 run execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s08 voice @s ~ ~ ~ 1 1 1
execute if score @s rpg_dt_t matches 30 run function rpg:daath_fight/morph/flake
execute if score @s rpg_dt_t matches 40 run function rpg:daath_fight/morph/flake
execute if score @s rpg_dt_t matches 50 run function rpg:daath_fight/morph/flake
execute if score @s rpg_dt_t matches 60 run function rpg:daath_fight/morph/flake
execute if score @s rpg_dt_t matches 70 run function rpg:daath_fight/morph/flake
execute if score @s rpg_dt_t matches 80 run function rpg:daath_fight/morph/flake
execute if score @s rpg_dt_t matches 90 run function rpg:daath_fight/morph/flake
execute if score @s rpg_dt_t matches 60 run execute on passengers if entity @s[tag=rpg.dtm.s.feet] run data merge entity @s {brightness:{block:15,sky:15}}
execute if score @s rpg_dt_t matches 60 run execute on passengers if entity @s[tag=rpg.dtm.s.legs] run data merge entity @s {brightness:{block:15,sky:15}}
execute if score @s rpg_dt_t matches 78 run execute on passengers if entity @s[tag=rpg.dtm.s.chest] run data merge entity @s {brightness:{block:15,sky:15}}
execute if score @s rpg_dt_t matches 92 run execute on passengers if entity @s[tag=rpg.dtm.s.head] run data merge entity @s {brightness:{block:15,sky:15}}
execute if score @s rpg_dt_t matches 100 run function rpg:daath/face/on
execute if score @s rpg_dt_t matches 100 run function rpg:daath/look/lit
execute if score @s rpg_dt_t matches 100 run function rpg:daath_fight/morph/crack
execute if score @s rpg_dt_t matches 112 run tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"selector":"@a[tag=rpg.dt.me,limit=1]","color":"#FFFFFF","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"面对面了。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　Face to face.","color":"#8F7430","bold":false,"italic":true}]
execute if score @s rpg_dt_t matches 112 run execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s09 voice @s ~ ~ ~ 1 1 1
execute if score @s rpg_dt_t matches 112 run function rpg:daath/anim/enter/hero
execute if score @s rpg_dt_t matches 140.. run function rpg:daath_fight/stage/begin2
