scoreboard players set @s rpg_jq_sk 6
scoreboard players set @s rpg_jq_t 0
scoreboard players set @s rpg_jq_busy 38
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
particle minecraft:cloud ~ ~0.2 ~ 0.4 0.05 0.4 0.02 10
playsound minecraft:entity.horse.gallop hostile @a[distance=..24] ~ ~ ~ 1 0.8
tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#F2F2F2","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"圣殿冲锋 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"为了圣殿！","color":"#9C9A94","bold":false,"italic":false}]
