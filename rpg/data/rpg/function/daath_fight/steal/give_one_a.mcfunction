execute store result storage rpg:daath t.id int 1 run scoreboard players get @s rpg_fg_id
function rpg:daath_fight/steal/give_a with storage rpg:daath t
tellraw @s ["",{"text":"[原质] ","color":"#C9A646","bold":true,"italic":false},{"text":"盔甲回到你手里。","color":"#AAB4C3","bold":false,"italic":false}]
