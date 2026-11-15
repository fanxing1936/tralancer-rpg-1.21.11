scoreboard players set @s rpg_jq_sk 9
scoreboard players set @s rpg_jq_t 0
scoreboard players set @s rpg_jq_busy 64
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:jacques/anim/enter/mighty
summon minecraft:marker ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.crossc","rpg.jqb.ult"]}
scoreboard players set @e[type=minecraft:marker,tag=rpg.jqb.crossc] rpg_jq_life 34
execute as @e[type=minecraft:marker,tag=rpg.jqb.crossc] run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rpg.jqb.crossc] at @s run function rpg:jacques_boss/cross/warn
playsound minecraft:block.anvil.land hostile @a[distance=..32] ~ ~ ~ 1 0.6
tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#F2F2F2","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔊𝔯𝔞𝔫𝔡 𝔐𝔞𝔰𝔱𝔢𝔯","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"十字审判 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"跪下，在十字之前。","color":"#9C9A94","bold":false,"italic":false}]
