scoreboard players set @s rpg_jq_sk 4
scoreboard players set @s rpg_jq_t 0
scoreboard players set @s rpg_jq_busy 26
scoreboard players add @s rpg_jq_n 1
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:jacques/weapon/harp1
function rpg:jacques/anim/enter/load
