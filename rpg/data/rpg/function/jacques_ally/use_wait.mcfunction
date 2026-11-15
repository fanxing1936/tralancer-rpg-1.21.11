scoreboard players operation #left rpg_al = @s rpg_al_cd
scoreboard players operation #left rpg_al -= #now rpg_al
scoreboard players add #left rpg_al 19
scoreboard players set #k rpg_al 20
scoreboard players operation #left rpg_al /= #k rpg_al
tellraw @s ["",{"text":"〖圣殿誓约〗","color":"#F0CF7A","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"号角还在回响。还需 ","color":"#9C9A94","bold":false,"italic":false},{"score":{"name":"#left","objective":"rpg_al"},"color":"#FFF2C8"},{"text":" 秒。","color":"#9C9A94","bold":false,"italic":false}]
