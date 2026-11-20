execute at @e[type=minecraft:marker,tag=rpg.slb.center,limit=1] run particle minecraft:flash{color:14212838} ~ ~2 ~ 0 0 0 0 1 force
execute at @e[type=minecraft:marker,tag=rpg.slb.center,limit=1] run particle minecraft:end_rod ~ ~4 ~ 3 3 3 0.02 60 force
execute at @e[type=minecraft:marker,tag=rpg.slb.center,limit=1] run playsound minecraft:block.bell.resonate hostile @a[distance=..48] ~ ~ ~ 1 0.6
execute at @e[type=minecraft:marker,tag=rpg.slb.center,limit=1] run tellraw @a[distance=..48] ["",{"text":"〖撒母耳记下 1:27〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"英雄何竟仆倒！战具何竟灭没！","color":"#E6DFCF","bold":false,"italic":false}]
function rpg:saul_boss/clear
