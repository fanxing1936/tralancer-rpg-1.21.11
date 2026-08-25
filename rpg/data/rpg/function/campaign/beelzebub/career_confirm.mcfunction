function rpg:campaign/beelzebub/complete_player
tag @s add rpg.ch1.career.confirmed
tellraw @s ["",{"text":"[道路确认] ","color":"#D4AF37","bold":true,"italic":false},{"text":"边缘者档案已归档；首通奖励与裁决记录已写入。","color":"gray","bold":false,"italic":false}]
