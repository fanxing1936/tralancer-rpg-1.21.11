scoreboard players set #pick rpg_l2_v 8
function rpg:lucifer_fight/p1/begin
scoreboard players set @s rpg_dm_cd 30
function rpg:lucifer_lord/play/cast
tellraw @a[distance=..48] ["",{"text":"〖路西法〗","color":"#34975A","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"晨星坠落 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"看哪，明亮之星，早晨之子，从天坠落。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:block.beacon.activate hostile @a[distance=..40] ~ ~ ~ 1.2 1.6
