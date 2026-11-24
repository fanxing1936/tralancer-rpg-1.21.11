# 玩家面板「序章」按钮（trigger rpg_pro_go，任何人随时可以进；as 玩家）
scoreboard players set @s rpg_pro_go 0
execute if entity @s[tag=rpg.ob] run return 0
execute if entity @s[tag=rpg.pr] run return 0
execute if score #state rpg_pr matches 1.. run return run tellraw @s ["",{"text":"[破碎大陆] ","color":"#FFD85A","bold":true,"italic":false},{"text":"序章正被其他人游玩，同一时间只能开一场，稍后再试。","color":"#9C9A94","bold":false,"italic":false}]
execute if score #fight rpg_mk matches 1 run return run tellraw @s ["",{"text":"[破碎大陆] ","color":"#FFD85A","bold":true,"italic":false},{"text":"有一场米迦勒战正在进行，结束后再进入序章。","color":"#9C9A94","bold":false,"italic":false}]
function rpg:onboard/pro/go
