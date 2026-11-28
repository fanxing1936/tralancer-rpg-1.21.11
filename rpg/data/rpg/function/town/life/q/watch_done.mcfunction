tellraw @s ["",{"text":"〖","color":"#A8B4C0","bold":true,"italic":false},{"text":"守夜人","color":"#A8B4C0","bold":true,"italic":false},{"text":"〗","color":"#A8B4C0","bold":true,"italic":false},{"text":" 𝔚𝔞𝔱𝔠𝔥𝔪𝔞𝔫","color":"#8F7430","italic":false},{"text":"  走完了？好。拿去，这是守夜的钱。","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"All the way round? Good. Here, a watchman's wage.","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.wt04 voice @s ~ ~ ~ 1 1
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
scoreboard players set @s rpg_tl_q3 0
scoreboard players operation @s rpg_tl_qd3 = #day1 rpg_tl
function rpg:town/life/rep_add {n:10}
tellraw @s ["",{"text":"〖委托完成〗","color":"#C9A646","bold":true,"italic":false},{"text":"  守夜人","color":"#E6DFCF","bold":true,"italic":false}]
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.3
function rpg:events/bt/town_quest
