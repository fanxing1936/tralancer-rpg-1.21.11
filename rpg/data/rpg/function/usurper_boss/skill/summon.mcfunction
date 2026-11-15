tag @s remove rpg.usb.auth
scoreboard players set @s rpg_ub_sk 14
scoreboard players set @s rpg_ub_t 0
scoreboard players set @s rpg_ub_busy 47
data merge entity @s {NoAI:1b}
function rpg:prime_enchanter/anim/enter/summon
playsound minecraft:block.beacon.power_select hostile @a[distance=..32] ~ ~ ~ 1.2 1.2
tellraw @a[distance=..48] ["",{"text":"〖篡夺者〗","color":"#F0CF7A","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"授权 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"起来，替我执行。","color":"#9C9A94","bold":false,"italic":false}]
