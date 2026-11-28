tellraw @s ["",{"text":"〖","color":"#E6DFCF","bold":true,"italic":false},{"text":"孩子","color":"#E6DFCF","bold":true,"italic":false},{"text":"〗","color":"#E6DFCF","bold":true,"italic":false},{"text":" ℭ𝔥𝔦𝔩𝔡","color":"#8F7430","italic":false},{"text":"  我们回家吧。我不怕了。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"Let's go home. I'm not scared any more.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ch04 voice @s ~ ~ ~ 1 1
scoreboard players set @s rpg_tl_q5 0
scoreboard players operation @s rpg_tl_qd5 = #day1 rpg_tl
function rpg:town/life/rep_add {n:15}
tellraw @s ["",{"text":"〖委托完成〗","color":"#C9A646","bold":true,"italic":false},{"text":"  失踪的孩子","color":"#E6DFCF","bold":true,"italic":false}]
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.3
function rpg:events/bt/town_quest
