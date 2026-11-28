execute if score @s rpg_tl_qd4 = #day1 rpg_tl run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  这件事今天已经做过了，明天再来。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_tl_q4 matches 6.. run return run function rpg:town/life/q/wheat_done
execute if score @s rpg_tl_q4 matches 1.. run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  去粮仓里面看看，待一会儿。","color":"#9C9A94","bold":false,"italic":false}]
tellraw @s ["",{"text":"〖","color":"#E6DFCF","bold":true,"italic":false},{"text":"村长","color":"#E6DFCF","bold":true,"italic":false},{"text":"〗","color":"#E6DFCF","bold":true,"italic":false},{"text":" 𝔉𝔞𝔯𝔪𝔴𝔦𝔣𝔢","color":"#8F7430","italic":false},{"text":"  你闻到没有？粮仓那边一股酸味，麦子都发黑了。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Can you smell it? Something sour by the granary. The grain's gone black.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.rb01 voice @s ~ ~ ~ 1 1
scoreboard players set @s rpg_tl_q4 1
tellraw @s ["",{"text":"〖委托〗","color":"#C9A646","bold":true,"italic":false},{"text":"  发黑的麦子","color":"#E6DFCF","bold":true,"italic":false},{"text":"　到粮仓里待一会儿，找出异味的来源","color":"#9C9A94","bold":false,"italic":false}]
