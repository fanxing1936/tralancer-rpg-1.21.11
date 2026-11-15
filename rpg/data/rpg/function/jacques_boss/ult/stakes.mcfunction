scoreboard players set @s rpg_jq_sk 14
scoreboard players set @s rpg_jq_t 0
scoreboard players set @s rpg_jq_busy 129
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:jacques/anim/enter/gong
function rpg:jacques/weapon/none
summon minecraft:marker ~ ~ ~ {Tags:["rpg.jqb.fx","rpg.jqb.stakec","rpg.jqb.ult"]}
scoreboard players set @e[type=minecraft:marker,tag=rpg.jqb.stakec] rpg_jq_life 131
execute as @e[type=minecraft:marker,tag=rpg.jqb.stakec] run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rpg.jqb.stakec] at @s run function rpg:jacques_boss/stakes/raise
playsound minecraft:block.bell.use hostile @a[distance=..40] ~ ~ ~ 2 0.5
function rpg:jacques_boss/vfx/ult2
tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#FF8A3D","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":" 𝔗𝔥𝔢 𝔅𝔲𝔯𝔫𝔦𝔫𝔤 𝔒𝔞𝔱𝔥","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"七座火刑柱 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"七座火刑柱。教廷给我的，我还给你。","color":"#9C9A94","bold":false,"italic":false}]
