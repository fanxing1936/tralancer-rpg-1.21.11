# 老存档：开局早就走完了，没有故乡 → 按国家分一座，不传送，只告诉一声
function rpg:town/home/pick
execute store result storage rpg:town h.i int 1 run scoreboard players get @s rpg_tw_home
function rpg:town/req with storage rpg:town h
tellraw @s ["",{"text":"〖故乡〗","color":"#C9A646","bold":true,"italic":false},{"text":"  大陆上建起了城镇。你出生的那一座，在你的国家境内；神父会在那里等你。","color":"#9C9A94","bold":false,"italic":false}]
