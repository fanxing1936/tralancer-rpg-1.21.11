loot give @s loot rpg:forge/rune_any
tellraw @s ["",{"text":"〖","color":"#E6DFCF","bold":true,"italic":false},{"text":"围观的少年","color":"#E6DFCF","bold":true,"italic":false},{"text":"〗","color":"#E6DFCF","bold":true,"italic":false},{"text":" 𝔏𝔞𝔡","color":"#8F7430","italic":false},{"text":"  你是怎么做到的？教教我！","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"How did you do that? Teach me!","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.th03 voice @s ~ ~ ~ 1 1
scoreboard players set @s rpg_tl_q9 0
scoreboard players operation @s rpg_tl_qd9 = #day1 rpg_tl
function rpg:town/life/rep_add {n:8}
tellraw @s ["",{"text":"〖委托完成〗","color":"#C9A646","bold":true,"italic":false},{"text":"  酒馆赌约","color":"#E6DFCF","bold":true,"italic":false}]
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.3
function rpg:events/bt/town_quest
