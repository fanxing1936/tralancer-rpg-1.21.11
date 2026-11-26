tag @p[tag=rpg.dt.in] add rpg.dt.me
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"text":"影","color":"#AAB4C3","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"别找门了。你每走一步，我都在。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　Stop looking for the door. I was there for every step.","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s02 voice @s ~ ~ ~ 1 1 1
tag @a remove rpg.dt.me
