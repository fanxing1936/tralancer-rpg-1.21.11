# 用完还回手里
advancement revoke @s only rpg:daath/shard
loot give @s loot rpg:daath/shard
scoreboard players add @s rpg_dt_de 0
scoreboard players add @s rpg_el_kill 0
scoreboard players add @s rpg_ex_rites 0
scoreboard players add @s rpg_ex_xp 0
scoreboard players add @s rpg_sef 0
scoreboard players add @s rpg_dt_win 0
tellraw @s ["",{"text":"〖碎镜〗","color":"#AAB4C3","bold":true,"italic":false},{"text":"　","color":"#FFFFFF","bold":false,"italic":false},{"text":"死过 ","color":"#9C9A94","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_dt_de"},"color":"#E6DFCF","bold":true},{"text":" 次　","color":"#9C9A94","bold":false,"italic":false},{"text":"杀过精英 ","color":"#9C9A94","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_el_kill"},"color":"#E6DFCF","bold":true},{"text":" 只　","color":"#9C9A94","bold":false,"italic":false},{"text":"裁决 ","color":"#9C9A94","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_ex_rites"},"color":"#E6DFCF","bold":true},{"text":" 次　","color":"#9C9A94","bold":false,"italic":false},{"text":"阅历 ","color":"#9C9A94","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_ex_xp"},"color":"#E6DFCF","bold":true},{"text":"　","color":"#9C9A94","bold":false,"italic":false},{"text":"原质 ","color":"#9C9A94","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_sef"},"color":"#E6DFCF","bold":true},{"text":" 阶　","color":"#9C9A94","bold":false,"italic":false},{"text":"下过深渊 ","color":"#9C9A94","bold":false,"italic":false},{"score":{"name":"@s","objective":"rpg_dt_win"},"color":"#E6DFCF","bold":true},{"text":" 次　","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:block.glass.place player @s ~ ~ ~ 1 0.6
