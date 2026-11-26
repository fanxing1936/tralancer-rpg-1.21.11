scoreboard players operation #s rpg_dt = @s rpg_dt_cd
scoreboard players set #k rpg_dt 20
scoreboard players operation #s rpg_dt /= #k rpg_dt
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"刚从深渊里上来，再等 ","color":"#E6DFCF","bold":false,"italic":false},{"score":{"name":"#s","objective":"rpg_dt"},"color":"#AAB4C3"},{"text":" 秒。","color":"#E6DFCF","bold":false,"italic":false}]
