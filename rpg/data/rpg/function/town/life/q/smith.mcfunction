execute if score @s rpg_tl_qd1 = #day1 rpg_tl run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  这件事今天已经做过了，明天再来。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_tl_q1 matches 1 if score @s rpg_tl_fu matches 1.. run return run function rpg:town/life/q/smith_done
execute if score @s rpg_tl_q1 matches 1 run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  还没熔过、拆过武器呢。营火工作台的「熔铸」「拆解」两页。","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players set @s rpg_tl_fu 0
scoreboard players set @s rpg_tl_q1 1
tellraw @s ["",{"text":"〖委托〗","color":"#C9A646","bold":true,"italic":false},{"text":"  铁匠的学徒","color":"#E6DFCF","bold":true,"italic":false},{"text":"　去营火旁熔铸或拆解一件武器","color":"#9C9A94","bold":false,"italic":false}]
