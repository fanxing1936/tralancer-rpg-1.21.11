scoreboard players set @s rpg_ub_sk 11
scoreboard players set @s rpg_ub_t 0
scoreboard players set @s rpg_ub_busy 81
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:prime_enchanter/anim/enter/launch
playsound minecraft:entity.breeze.jump hostile @a[distance=..32] ~ ~ ~ 1.2 0.6
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#F0CF7A","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"天降 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"……从天上。","color":"#9C9A94","bold":false,"italic":false}]
