execute if score @s rpg_mk_i3 matches 1 if score #w rpg_mk_i3 matches 2.. run return run function rpg:michael_boss_i3/skill/quis
execute if score @s rpg_mk_i3 matches 2 if score #w rpg_mk_i3 matches 3.. run return run function rpg:michael_boss_i3/skill/dash
scoreboard players set @s rpg_mk_sk 8
scoreboard players set @s rpg_mk_t 0
scoreboard players set @s rpg_mk_busy 34
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score @s rpg_mk_i3 matches 1 run function rpg:michael/anim/enter/mighty
execute if score @s rpg_mk_i3 matches 2 run function rpg:michael/anim/enter/hero
execute if score @s rpg_mk_i3 matches 1 run execute unless score #pro rpg_mk_i3 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"天使长 ","color":"#FFD0BD","bold":true,"italic":false},{"text":"米迦勒","color":"#FFF5EE","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":" 𝔇𝔞𝔫𝔦𝔢𝔩 4:13","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"守望者降临 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"守望的圣者，从天而降。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_mk_i3 matches 2.. run execute unless score #pro rpg_mk_i3 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":" 𝔇𝔞𝔫𝔦𝔢𝔩 4:13","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"守望者降临 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"守望的圣者，从天而降。","color":"#9C9A94","bold":false,"italic":false}]
