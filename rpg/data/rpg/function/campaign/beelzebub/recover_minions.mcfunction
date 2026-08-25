tag @e[tag=rpg.ch1.minion] remove rpg.ch1.minion.current
execute as @e[tag=rpg.ch1.minion] if score @s rpg_ch1_id = @e[type=minecraft:marker,tag=rpg.ch1.controller,limit=1] rpg_ch1_id run tag @s add rpg.ch1.minion.current
kill @e[tag=rpg.ch1.minion.current]
tag @s remove rpg.ch1.mira.captured
scoreboard players set @s rpg_ch1_empty 0
scoreboard players add @s rpg_ch1_fail 1
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[章节恢复] ","color":"#B8A98B","bold":true,"italic":false},{"text":"罪仆归属未完整建立，重新展开这一波。","color":"gray","bold":false,"italic":false}]
scoreboard players set @s rpg_ch1_time 0
function rpg:campaign/beelzebub/stage/3_enter
