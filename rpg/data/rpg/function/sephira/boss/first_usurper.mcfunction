scoreboard players add @s rpg_bkd_usurper 1
scoreboard players add @s rpg_ex_xp 80
scoreboard players add @s rpg_sp 1
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"首次击败","color":"#9C9A94","bold":false,"italic":false},{"text":"篡夺者","color":"#C9A646","bold":true,"italic":false},{"text":" · 阅历 +80 · 技能点 +1","color":"#E6DFCF","bold":false,"italic":false}]
function rpg:world/boss/first_usurper
