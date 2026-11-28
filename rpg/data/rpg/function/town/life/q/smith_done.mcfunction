scoreboard players set @s rpg_tl_q1 0
scoreboard players operation @s rpg_tl_qd1 = #day1 rpg_tl
function rpg:town/life/rep_add {n:10}
tellraw @s ["",{"text":"〖委托完成〗","color":"#C9A646","bold":true,"italic":false},{"text":"  铁匠的学徒","color":"#E6DFCF","bold":true,"italic":false}]
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.5 1.3
function rpg:events/bt/town_quest
loot give @s loot rpg:forge/item/blank
loot give @s loot rpg:forge/item/forge_stone
loot give @s loot rpg:forge/item/soul
