function rpg:daath_fight/sk/end
data merge entity @s {NoAI:1b,Invulnerable:1b}
function rpg:daath/anim/enter/hero
execute at @a[tag=rpg.dt.me,limit=1] run tp @s ^ ^ ^1.2 facing entity @a[tag=rpg.dt.me,limit=1] feet
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"text":"影","color":"#AAB4C3","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"再看一遍。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　Look again.","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s21 voice @s ~ ~ ~ 1 1 1
playsound minecraft:block.conduit.deactivate hostile @a[distance=..48] ~ ~ ~ 1 0.5
