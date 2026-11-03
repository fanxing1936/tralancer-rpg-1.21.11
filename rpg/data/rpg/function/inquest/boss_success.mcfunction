execute on passengers run kill @s
particle sculk_soul ~ ~1 ~ 1.2 1.4 1.2 0.16 80 normal
particle end_rod ~ ~1 ~ 1.4 1.2 1.4 0.12 80 normal
particle flash{color:16777215} ~ ~1 ~ 0 0 0 0 1 normal
playsound minecraft:entity.wither.death hostile @a[distance=..40] ~ ~ ~ 1 1.45
experience add @a[distance=..10,gamemode=!spectator] 80 points
scoreboard players remove @a[distance=..10,gamemode=!spectator] rpg_taint 10
scoreboard players set @a[distance=..10,gamemode=!spectator,scores={rpg_taint=..-1}] rpg_taint 0
tellraw @a[distance=..24,gamemode=!spectator] ["",{"text":"〖驱魔完成〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔈𝔵𝔬𝔯𝔠𝔦𝔰𝔢𝔡","color":"#836C2E","bold":false,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"真名已宣、罪性已断，恶魔被逐离此世。","color":"#E6DFCF","italic":false}]
kill @s
