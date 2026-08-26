tag @s remove rpg.ch1.puzzle.wait.route
scoreboard players set @s rpg_ch1_choice 0
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[安全复盘] ","color":"#B8A98B","bold":true,"italic":false},{"text":"战斗结束。三份记录已重新展开，可以继续推理。","color":"gray","bold":false,"italic":false}]
function rpg:campaign/beelzebub/route/spawn_choices
