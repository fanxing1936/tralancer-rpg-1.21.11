scoreboard players set @s rpg_ub_sk 13
scoreboard players set @s rpg_ub_t 0
scoreboard players set @s rpg_ub_busy 112
data merge entity @s {NoAI:1b}
execute facing entity @e[tag=rpg.unit.f,distance=..25,sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rpg:prime_enchanter/anim/enter/lightning_slam
playsound minecraft:block.beacon.power_select hostile @a[distance=..32] ~ ~ ~ 1 1.8
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#F0CF7A","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"圣雷砸地 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"雷霆在我手里。","color":"#9C9A94","bold":false,"italic":false}]
