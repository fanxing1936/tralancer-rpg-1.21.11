tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"selector":"@a[tag=rpg.dt.me,limit=1]","color":"#FFFFFF","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"你连自己都不认识。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　You do not even know yourself.","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s13 voice @s ~ ~ ~ 1 1 1
kill @e[tag=rpg.dt.card,distance=..60]
tag @a[tag=rpg.dt.me,limit=1] add rpg.dt.hit
execute if entity @a[tag=rpg.dt.hit] run scoreboard players set #pc rpg_dt 20
execute if entity @a[tag=rpg.dt.hit] run function rpg:daath_fight/hurt/all
function rpg:daath_fight/sk/end
scoreboard players set @s rpg_dt_gap 30
