execute store result storage rpg:onboard tmp.id int 1 run scoreboard players get @s rpg_fg_id
# 进入旁白（as 玩家）；已经在放就不重来（「重新打开」点到这里时）
execute if entity @s[tag=rpg.ob.intro] run return 0
tag @s add rpg.ob.intro
scoreboard players set @s rpg_ob_it 0
function rpg:onboard/intro/bars with storage rpg:onboard tmp
function rpg:onboard/music/intro
tellraw @s ["",{"text":"[破碎大陆] ","color":"#FFD85A","bold":true,"italic":false},{"text":"旁白约一分钟。","color":"#9C9A94","bold":false,"italic":false},{"text":"[跳过旁白]","color":"#FFD85A","underlined":true,"bold":false,"italic":false,"click_event":{"action":"run_command","command":"/trigger rpg_ob_do set 98"}}]
