scoreboard players set #blood rpg_pf 400
tag @e[type=minecraft:vindicator,tag=rpg.pf.unit,sort=nearest,limit=1] add rpg.pf.sac
tellraw @a[distance=..48] ["",{"text":"〖教皇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"为圣座流血吧，孩子。","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players set #sk rpg_pf 4
scoreboard players set #st rpg_pf 0
function rpg:pope_fight/clip/cast
execute positioned ^0.43 ^2.90 ^0.57 run function rpg:pope_fight/fx/charge
playsound rpg:pope.load_spell hostile @a[distance=..32] ~ ~ ~ 0.7 1
