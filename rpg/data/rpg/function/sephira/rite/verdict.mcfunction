# 一次驱魔裁决完成（封印 / 立约 / 消灭）
scoreboard players add @s rpg_ex_rites 1
scoreboard players add @s rpg_ex_xp 10
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"裁决完成 · 阅历 +10 · 驱魔熟练按裁决次数提升","color":"#E6DFCF","bold":false,"italic":false}]
function rpg:quest/hook/verdict
