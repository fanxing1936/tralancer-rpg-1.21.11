execute at @e[type=minecraft:marker,tag=rpg.lub.center,limit=1] run particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:3} ~ ~2 ~ 3 2 3 0.1 120 force
execute at @e[type=minecraft:marker,tag=rpg.lub.center,limit=1] run playsound minecraft:entity.wither.death hostile @a[distance=..48] ~ ~ ~ 1 1.3
execute at @e[type=minecraft:marker,tag=rpg.lub.center,limit=1] run tellraw @a[distance=..48] ["",{"text":"〖启示录 20:2〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"他捉住那龙，就是古蛇，又叫魔鬼，也叫撒但，把它捆绑一千年。","color":"#E6DFCF","bold":false,"italic":false}]
execute at @e[type=minecraft:marker,tag=rpg.lub.center,limit=1] run scoreboard players set @e[tag=rpg.unit,distance=..48] rpg_taint 0
function rpg:lucifer_boss/clear
