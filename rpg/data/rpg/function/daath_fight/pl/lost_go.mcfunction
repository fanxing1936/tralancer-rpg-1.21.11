scoreboard players add @s rpg_dt_n 1
function rpg:daath_fight/pl/out
scoreboard players set @s rpg_dt_cd 2400
effect give @s minecraft:regeneration 8 3 true
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"你被送了回来。两分钟后可以再来。","color":"#E6DFCF","bold":false,"italic":false}]
execute if score @s rpg_dt_n matches 1 run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"提示：眼睛里显示的是它记住了什么。别总用同一招。","color":"#AAB4C3","bold":false,"italic":false}]
execute if score @s rpg_dt_n matches 2 run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"提示：打亮灯柱，它走进光里才会显形。","color":"#AAB4C3","bold":false,"italic":false}]
execute if score @s rpg_dt_n matches 3 run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"提示：地上先亮的线、圈、影子，都是它要打的地方。","color":"#AAB4C3","bold":false,"italic":false}]
execute if score @s rpg_dt_n matches 4 run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"提示：夺走的东西：灯下打中它四下，或者让它眩晕，就能拿回来。","color":"#AAB4C3","bold":false,"italic":false}]
execute if score @s rpg_dt_n matches 5 run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"提示：「同一把剑」亮到最亮的那一瞬间出手。","color":"#AAB4C3","bold":false,"italic":false}]
execute if score @s rpg_dt_n matches 6.. run tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"提示：打法越单一，它越强。","color":"#AAB4C3","bold":false,"italic":false}]
