scoreboard players set @s rpg_jq_sk 15
scoreboard players set @s rpg_jq_t 0
scoreboard players set @s rpg_jq_busy 96
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:jacques_boss/vfx/ult2
tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#FF8A3D","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔅𝔲𝔯𝔫𝔦𝔫𝔤 𝔒𝔞𝔱𝔥","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"最后的冲锋 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"最后一次——为了圣殿。","color":"#9C9A94","bold":false,"italic":false}]
