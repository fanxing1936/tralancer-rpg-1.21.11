# 累计击杀 100 名精英：第 7 源质「胜利」
execute if entity @s[tag=rpg.wl.victory] run return 0
tag @s add rpg.wl.victory
function rpg:world/kab/line_9
tellraw @s ["",{"text":"[秘仪]","color":"#D596F2","bold":true,"italic":false},{"text":"　第一百名精英倒下。你得到了源质「胜利」。","color":"#9C9A94","bold":false,"italic":false}]
