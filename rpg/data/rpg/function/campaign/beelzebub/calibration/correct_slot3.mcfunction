tag @s add rpg.ch1.slot.3
kill @e[type=minecraft:text_display,tag=rpg.ch1.slot3.label,distance=..72]
kill @e[type=minecraft:marker,tag=rpg.ch1.slot3,distance=..72]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[槽位校准] ","color":"#62D9E8","bold":true,"italic":false},{"text":"待确证残页保留见证空位","color":"gray","bold":false,"italic":false}]
function rpg:campaign/beelzebub/calibration/check_complete
