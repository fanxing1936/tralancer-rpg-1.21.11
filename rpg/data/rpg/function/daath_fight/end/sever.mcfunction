execute if score @s rpg_dt_t matches 4 run tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"selector":"@a[tag=rpg.dt.me,limit=1]","color":"#FFFFFF","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……好。那就一个人走吧。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　...Very well. Walk on alone.","color":"#8F7430","bold":false,"italic":true}]
execute if score @s rpg_dt_t matches 4 run execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s19 voice @s ~ ~ ~ 1 1 1
execute if score @s rpg_dt_t matches 4 run function rpg:daath_fight/end/cut
execute if score @s rpg_dt_t matches 26 run function rpg:daath/anim/enter/fall
execute if score @s rpg_dt_t matches 30..60 run function rpg:daath_fight/end/flake
execute if score @s rpg_dt_t matches 62 run function rpg:daath_fight/end/finish
