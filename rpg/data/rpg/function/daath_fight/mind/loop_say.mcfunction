# 这句半分钟最多说一次
scoreboard players operation @s rpg_dt_say = @s rpg_dt_orb
scoreboard players add @s rpg_dt_say 600
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"text":"影","color":"#AAB4C3","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"又是这一招。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　Again.","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s04 voice @s ~ ~ ~ 1 1 1
