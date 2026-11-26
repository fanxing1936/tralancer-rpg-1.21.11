tag @s remove rpg.dt.right
tellraw @a[tag=rpg.dt.me,limit=1] ["",{"text":"〖","color":"#7C8593","bold":true,"italic":false},{"selector":"@a[tag=rpg.dt.me,limit=1]","color":"#FFFFFF","bold":true,"italic":false},{"text":"〗","color":"#7C8593","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"是。","color":"#E6DFCF","bold":false,"italic":false},{"text":"　Yes.","color":"#8F7430","bold":false,"italic":true}]
execute as @a[tag=rpg.dt.me,limit=1] at @s run playsound rpg:vo.daath.s12 voice @s ~ ~ ~ 1 1 1
kill @e[tag=rpg.dt.card,distance=..60]
scoreboard players set #s rpg_dt 100
function rpg:daath_fight/stun
playsound minecraft:block.beacon.power_select hostile @a[distance=..48] ~ ~ ~ 1 1.4
