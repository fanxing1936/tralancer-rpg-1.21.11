scoreboard players set @s rpg_ex_choice 0
tellraw @s ["",{"text":"[裁决拒绝] ","color":"#8B2500","bold":true,"italic":false},{"text":"你不是当前章节的登记成员，或档案编号与法阵不符。","color":"gray","bold":false,"italic":false}]
playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.7 0.6
