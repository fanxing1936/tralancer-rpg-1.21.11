scoreboard players set @s rpg_mk_sk 19
scoreboard players set @s rpg_mk_t 0
scoreboard players set @s rpg_mk_busy 238
data merge entity @s {NoAI:1b,NoGravity:1b}
tag @s add rpg.mkb.air
tp @s @e[type=minecraft:marker,tag=rpg.mkb.center,limit=1,distance=0..]
function rpg:michael/anim/enter/rise
execute if score @s rpg_mk_i1 matches 1 run execute unless score #pro rpg_mk_i1 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"天使长 ","color":"#FFD0BD","bold":true,"italic":false},{"text":"米迦勒","color":"#FFF5EE","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":" ℜ𝔢𝔳𝔢𝔩𝔞𝔱𝔦𝔬𝔫 12:4","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"三分之一的星辰 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"三分之一的星辰，从天上坠落。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_mk_i1 matches 2.. run execute unless score #pro rpg_mk_i1 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":" ℜ𝔢𝔳𝔢𝔩𝔞𝔱𝔦𝔬𝔫 12:4","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"三分之一的星辰 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"三分之一的星辰，从天上坠落。","color":"#9C9A94","bold":false,"italic":false}]
function rpg:michael_boss_i1/stars/which
