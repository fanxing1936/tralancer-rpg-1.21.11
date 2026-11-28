clear @s minecraft:potion[minecraft:potion_contents={potion:"minecraft:water"}] 1
clear @s minecraft:sugar 2
clear @s minecraft:charcoal 1
tellraw @s ["",{"text":"〖","color":"#C9A646","bold":true,"italic":false},{"text":"神父","color":"#C9A646","bold":true,"italic":false},{"text":"〗","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔉𝔞𝔱𝔥𝔢𝔯","color":"#8F7430","italic":false},{"text":"  这瓶圣水是你自己炼的。比我给你的那瓶更管用。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"You made this holy water yourself. It'll serve you better than any I could give.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.pr20 voice @s ~ ~ ~ 1 1
function rpg:alc/give/holy
function rpg:alc/give/holy
scoreboard players set @s rpg_tl_q2 0
scoreboard players operation @s rpg_tl_qd2 = #day1 rpg_tl
function rpg:town/life/rep_add {n:10}
tellraw @s ["",{"text":"〖委托完成〗","color":"#C9A646","bold":true,"italic":false},{"text":"  神父的圣水","color":"#E6DFCF","bold":true,"italic":false}]
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.3
function rpg:events/bt/town_quest
