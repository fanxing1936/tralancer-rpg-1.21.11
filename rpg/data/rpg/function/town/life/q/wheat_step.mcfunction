particle minecraft:dust{color:[0.35,0.42,0.12],scale:1.2} ~ ~1 ~ 2 1 2 0 20
playsound minecraft:entity.bee.loop hostile @s ~ ~ ~ 0.4 0.6
scoreboard players add @s rpg_tl_q4 1
execute if score @s rpg_tl_q4 matches 6 run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  麦袋从里面烂了，地上爬着一串苍蝇……回去告诉村长。","color":"#C9A646","bold":false,"italic":false}]
