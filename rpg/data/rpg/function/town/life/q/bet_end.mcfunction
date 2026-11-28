tag @s remove rpg.tl.bet
execute if score @s rpg_tl_hit matches 5.. run return run function rpg:town/life/q/bet_win
scoreboard players set @s rpg_tl_q9 0
tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  没打全。明天再来比。","color":"#FF6B5E","bold":false,"italic":false}]
scoreboard players operation @s rpg_tl_qd9 = #day1 rpg_tl
