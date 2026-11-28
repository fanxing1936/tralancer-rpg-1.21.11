execute if score @s rpg_tl_qd2 = #day1 rpg_tl run return run tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  这件事今天已经做过了，明天再来。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_tl_q2 matches 0 run return run function rpg:town/life/q/holy_take
execute store result score #a rpg_tl run clear @s minecraft:potion[minecraft:potion_contents={potion:"minecraft:water"}] 0
execute store result score #b rpg_tl run clear @s minecraft:sugar 0
execute store result score #c rpg_tl run clear @s minecraft:charcoal 0
execute if score #a rpg_tl matches 1.. if score #b rpg_tl matches 2.. if score #c rpg_tl matches 1.. run return run function rpg:town/life/q/holy_done
tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  要一瓶水、两份糖（当海盐）、一块木炭（圣火的灰）。","color":"#9C9A94","bold":false,"italic":false}]
