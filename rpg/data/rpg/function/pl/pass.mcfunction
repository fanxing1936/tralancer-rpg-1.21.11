# 失乐园通行符：第一次进门给 20 分钟「伊甸余晖」（受到的伤害降低）
clear @s minecraft:paper[minecraft:custom_data~{rpg_eden_pass:1b}] 1
effect give @s minecraft:resistance 1200 0
tellraw @s ["",{"text":"〖伊甸余晖〗","color":"#E0483C","bold":true,"italic":false},{"text":"  通行符化成一层薄光罩住你。二十分钟内受到的伤害降低。","color":"#9C9A94","bold":false,"italic":false}]
