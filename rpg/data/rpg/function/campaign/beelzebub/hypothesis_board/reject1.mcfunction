tag @s add rpg.ch1.theory.1
kill @e[type=minecraft:text_display,tag=rpg.ch1.theory1.label,distance=..72]
kill @e[type=minecraft:marker,tag=rpg.ch1.theory1,distance=..72]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[伪解排除] ","color":"#62D9E8","bold":true,"italic":false},{"text":"疫病复生","color":"gray","bold":false,"italic":false}]
function rpg:campaign/beelzebub/hypothesis_board/check_complete
