tag @s remove rpg.tl.kept
execute store result storage rpg:town k.id int 1 run scoreboard players get @s rpg_fg_id
scoreboard players set #n rpg_tl 0
function rpg:town/life/regive1 with storage rpg:town k
tellraw @s ["",{"text":"〖城镇〗","color":"#C9A646","bold":true,"italic":false},{"text":"  圣火替你收着的东西，都还给你了。","color":"#C9A646","bold":false,"italic":false}]
