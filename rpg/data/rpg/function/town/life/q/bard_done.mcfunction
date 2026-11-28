scoreboard players set @s rpg_tl_q6 0
scoreboard players operation @s rpg_tl_qd6 = #day1 rpg_tl
function rpg:town/life/rep_add {n:10}
tellraw @s ["",{"text":"〖委托完成〗","color":"#C9A646","bold":true,"italic":false},{"text":"  吟游诗人","color":"#E6DFCF","bold":true,"italic":false}]
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.3
function rpg:events/bt/town_quest
function rpg:quest/title/get_bard
