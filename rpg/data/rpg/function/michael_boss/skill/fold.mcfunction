scoreboard players set @s rpg_mk_sk 6
scoreboard players set @s rpg_mk_t 0
scoreboard players set @s rpg_mk_busy 64
data merge entity @s {NoAI:1b}
function rpg:michael/anim/enter/fold
tag @s add rpg.mkb.fold
execute if score @s rpg_mk matches 1 run execute unless score #pro rpg_mk matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"天使长 ","color":"#FFD0BD","bold":true,"italic":false},{"text":"米迦勒","color":"#FFF5EE","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":" ℑ𝔰𝔞𝔦𝔞𝔥 6:2","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"六翼掩面 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"用两个翅膀遮脸。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_mk matches 2.. run execute unless score #pro rpg_mk matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":" ℑ𝔰𝔞𝔦𝔞𝔥 6:2","color":"#8F7430","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"六翼掩面 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"用两个翅膀遮脸。","color":"#9C9A94","bold":false,"italic":false}]
