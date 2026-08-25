tag @s remove rpg.ch1.accepted
tag @s remove rpg.ch1.member
tag @s remove rpg.ch1.party
tag @s remove rpg.ch1.current
tag @s remove rpg.ch1.host
tag @s remove rpg.ch1.kit.issued
tag @s remove rpg.ch1.career.confirmed
scoreboard players set @s rpg_ch1_id 0
scoreboard players set @s rpg_ch1_session 0
tellraw @s ["",{"text":"[章节档案整理] ","color":"#B8A98B","bold":true,"italic":false},{"text":"已移除上一次实例遗留的临时参与状态；永久进度保留。","color":"gray","bold":false,"italic":false}]
