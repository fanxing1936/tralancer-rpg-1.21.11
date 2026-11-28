scoreboard players set @s rpg_mk_sk 9
scoreboard players set @s rpg_mk_t 0
scoreboard players set @s rpg_mk_busy 84
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:michael/anim/enter/hero
playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..48] ~ ~ ~ 1 0.8
execute if score @s rpg_mk_i1 matches 1 run execute unless score #pro rpg_mk_i1 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"天使长 ","color":"#FFD0BD","bold":true,"italic":false},{"text":"米迦勒","color":"#FFF5EE","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"注视 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"众目都看着你。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_mk_i1 matches 2.. run execute unless score #pro rpg_mk_i1 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"注视 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"众目都看着你。","color":"#9C9A94","bold":false,"italic":false}]
function rpg:michael_boss_i1/vfx/wings
