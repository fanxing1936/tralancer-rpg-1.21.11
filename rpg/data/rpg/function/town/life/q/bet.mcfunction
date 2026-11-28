execute if score @s rpg_tl_qd9 = #day1 rpg_tl run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  这件事今天已经做过了，明天再来。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_tl_q9 matches 1 run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  靶子还立着，快打！","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players set @s rpg_tl_hit 0
scoreboard players set @s rpg_tl_q9 1
tag @s add rpg.tl.bet
execute positioned ^-4 ^ ^6 positioned over motion_blocking_no_leaves run function rpg:town/life/q/target
execute positioned ^-2 ^ ^8 positioned over motion_blocking_no_leaves run function rpg:town/life/q/target
execute positioned ^0 ^ ^10 positioned over motion_blocking_no_leaves run function rpg:town/life/q/target
execute positioned ^2 ^ ^8 positioned over motion_blocking_no_leaves run function rpg:town/life/q/target
execute positioned ^4 ^ ^6 positioned over motion_blocking_no_leaves run function rpg:town/life/q/target
tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  三十秒，五个靶子。左键打中它们。","color":"#C9A646","bold":false,"italic":false}]
