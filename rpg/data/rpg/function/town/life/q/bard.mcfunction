execute if score @s rpg_tl_qd6 = #day1 rpg_tl run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  这件事今天已经做过了，明天再来。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_tl_q6 matches 8 run return run function rpg:town/life/q/bard_done
execute if score @s rpg_tl_q6 matches 1.. run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  还没听全：天使像、墓地、林中营地。","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players set @s rpg_tl_bd 0
scoreboard players set @s rpg_tl_q6 1
tellraw @s ["",{"text":"〖委托〗","color":"#C9A646","bold":true,"italic":false},{"text":"  吟游诗人","color":"#E6DFCF","bold":true,"italic":false},{"text":"　在天使像、墓地、林中营地各听一段歌","color":"#9C9A94","bold":false,"italic":false}]
