scoreboard players set @s rpg_ch1_sub 1
scoreboard players set @s rpg_ch1_time 0
tag @s remove rpg.ch1.slot.1
tag @s remove rpg.ch1.slot.2
tag @s remove rpg.ch1.slot.3
bossbar set rpg:chapter1 name ["",{"text":"仪式校准｜手持对应器具踏入三槽","color":"#D4AF37","bold":true,"italic":false}]
tellraw @a[tag=rpg.ch1.current] ["",{"text":"[仪式校准] ","color":"#D4AF37","bold":true,"italic":false},{"text":"边界槽用银质圣钉；腐宴槽用别西卜媒介；见证槽用待确证残页。器具不会消耗。","color":"gray","bold":false,"italic":false}]
function rpg:campaign/beelzebub/calibration/spawn_choices
