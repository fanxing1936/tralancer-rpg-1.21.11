scoreboard players set @s rpg_jq_sk 13
scoreboard players set @s rpg_jq_t 0
scoreboard players set @s rpg_jq_busy 24
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:jacques/anim/enter/curse
tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#FF8A3D","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"莫莱的诅咒 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"我以火刑柱起誓——你也一样。","color":"#9C9A94","bold":false,"italic":false}]
