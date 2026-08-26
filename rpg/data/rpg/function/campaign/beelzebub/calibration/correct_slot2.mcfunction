tag @s add rpg.ch1.slot.2
kill @e[type=minecraft:text_display,tag=rpg.ch1.slot2.label,distance=..72]
kill @e[type=minecraft:marker,tag=rpg.ch1.slot2,distance=..72]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[槽位校准] ","color":"#62D9E8","bold":true,"italic":false},{"text":"腐败媒介让饕宴拒食","color":"gray","bold":false,"italic":false}]
function rpg:campaign/beelzebub/calibration/check_complete
