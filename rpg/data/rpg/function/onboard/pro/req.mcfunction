# 玩家面板「序章」按钮（trigger rpg_pro_go，任何人随时可以再打一遍；as 玩家）
scoreboard players set @s rpg_pro_go 0
execute if entity @s[tag=rpg.ob] run return 0
execute if entity @s[tag=rpg.pr] run return 0
execute if entity @s[tag=rpg.pr.q] run return run tellraw @s ["",{"text":"[破碎大陆] ","color":"#FFD85A","bold":true,"italic":false},{"text":"你已经在序章的队伍里了，凑齐同伴就会开始。","color":"#9C9A94","bold":false,"italic":false}]
function rpg:prologue/enqueue
tellraw @s ["",{"text":"[破碎大陆] ","color":"#FFD85A","bold":true,"italic":false},{"text":"已排进序章的队伍：凑满四人，或稍等片刻没有别人，就会开始。","color":"#9C9A94","bold":false,"italic":false}]
