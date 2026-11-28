execute if score @s rpg_tl_qd3 = #day1 rpg_tl run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  这件事今天已经做过了，明天再来。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_tl_q3 matches 16 run return run function rpg:town/life/q/watch_done
execute if score @s rpg_tl_q3 matches 1.. run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  四处还没走完：墓地、刑台广场、教堂门口、营火。","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players set @s rpg_tl_wt 0
tellraw @s ["",{"text":"〖","color":"#A8B4C0","bold":true,"italic":false},{"text":"守夜人","color":"#A8B4C0","bold":true,"italic":false},{"text":"〗","color":"#A8B4C0","bold":true,"italic":false},{"text":" 𝔚𝔞𝔱𝔠𝔥𝔪𝔞𝔫","color":"#8F7430","italic":false},{"text":"  夜里绕镇走一圈。看见什么都别出声，回来告诉我。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Walk the town once tonight. Whatever you see, keep quiet and tell me.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.wt01 voice @s ~ ~ ~ 1 1
scoreboard players add #sid rpg_say 1
scoreboard players operation @s rpg_say = #sid rpg_say
execute store result score #due rpg_say run time query gametime
scoreboard players add #due rpg_say 126
function rpg:town/say/push {f:18}
scoreboard players set @s rpg_tl_q3 1
tellraw @s ["",{"text":"〖委托〗","color":"#C9A646","bold":true,"italic":false},{"text":"  守夜人","color":"#E6DFCF","bold":true,"italic":false},{"text":"　夜里走到墓地、刑台广场、教堂门口、营火四处","color":"#9C9A94","bold":false,"italic":false}]
