execute if score @s rpg_tl_qd5 = #day1 rpg_tl run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  这件事今天已经做过了，明天再来。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_tl_q5 matches 2 run return run function rpg:town/life/q/child_done
execute if score @s rpg_tl_q5 matches 1 run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  孩子在镇外的林子里。往没有路的地方找。","color":"#9C9A94","bold":false,"italic":false}]
execute as @e[type=minecraft:marker,tag=rpg.tw.at.camp] if score @s rpg_tw_id = #t rpg_tl at @s unless entity @e[type=minecraft:villager,tag=rpg.tnpc.child,distance=..12] positioned ~3 ~ ~3 run function rpg:town/life/q/child_spawn
scoreboard players set @s rpg_tl_q5 1
tellraw @s ["",{"text":"〖委托〗","color":"#C9A646","bold":true,"italic":false},{"text":"  失踪的孩子","color":"#E6DFCF","bold":true,"italic":false},{"text":"　到镇外林子里找一个迷路的孩子","color":"#9C9A94","bold":false,"italic":false}]
