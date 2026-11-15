scoreboard players set @s rpg_jq_sk 10
scoreboard players set @s rpg_jq_t 0
scoreboard players set @s rpg_jq_busy 98
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:jacques/weapon/harp4
function rpg:jacques/anim/enter/showoff
summon minecraft:marker ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.harpc","rpg.jqb.ult"]}
scoreboard players set @e[type=minecraft:marker,tag=rpg.jqb.harpc] rpg_jq_life 3
execute as @e[type=minecraft:marker,tag=rpg.jqb.harpc] run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rpg.jqb.harpc] at @s run function rpg:jacques_boss/harp/lay
tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#F2F2F2","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔊𝔯𝔞𝔫𝔡 𝔐𝔞𝔰𝔱𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"竖琴之弦 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"听啊，这是圣殿的琴。","color":"#9C9A94","bold":false,"italic":false}]
