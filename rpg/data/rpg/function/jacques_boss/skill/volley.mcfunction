scoreboard players set @s rpg_jq_sk 5
scoreboard players set @s rpg_jq_t 0
scoreboard players set @s rpg_jq_busy 34
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:jacques/weapon/harp1
function rpg:jacques/anim/enter/load
execute if score @s rpg_jq matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#F2F2F2","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"竖琴连弩 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"弦已上紧。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_jq matches 2 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#FF8A3D","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"燃火连弩 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"火，是从弦上来的。","color":"#9C9A94","bold":false,"italic":false}]
