execute store result storage rpg:onboard tmp.id int 1 run scoreboard players get @s rpg_fg_id
# 进黑屏：旁观、失明、升到原地上空（周围什么都没有，失明的雾把画面压成全黑）
tag @s add rpg.ob.hold
gamemode spectator @s
effect clear @s
effect give @s minecraft:blindness infinite 0 true
function rpg:onboard/hold/tp_go with storage rpg:onboard tmp
stopsound @s music
title @s clear
tellraw @s ["",{"text":"[破碎大陆] ","color":"#FFD85A","bold":true,"italic":false},{"text":"界面不见了？","color":"#9C9A94","bold":false,"italic":false},{"text":"[点这里重新打开]","color":"#FFD85A","underlined":true,"bold":false,"italic":false,"click_event":{"action":"run_command","command":"/trigger rpg_ob_do set 99"}}]
