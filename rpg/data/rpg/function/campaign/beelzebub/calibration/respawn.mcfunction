tag @s remove rpg.ch1.puzzle.wait.slot
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[安全复盘] ","color":"#B8A98B","bold":true,"italic":false},{"text":"错置回响已清除；三件器具仍在背包，槽位重新展开。","color":"gray","bold":false,"italic":false}]
function rpg:campaign/beelzebub/calibration/spawn_choices
