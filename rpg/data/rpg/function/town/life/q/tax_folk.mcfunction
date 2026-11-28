execute if score @s rpg_tl_qd8 = #day1 rpg_tl run return 0
scoreboard players remove @s rpg_tl_ch 10
tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  麦子藏进了地窖。镇上的人记住了你。","color":"#D596F2","bold":false,"italic":false}]
scoreboard players set @s rpg_tl_q8 0
scoreboard players operation @s rpg_tl_qd8 = #day1 rpg_tl
function rpg:town/life/rep_add {n:15}
tellraw @s ["",{"text":"〖委托完成〗","color":"#C9A646","bold":true,"italic":false},{"text":"  收税官","color":"#E6DFCF","bold":true,"italic":false}]
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.3
function rpg:events/bt/town_quest
