tag @s add rpg.wl.book
execute if score @s rpg_ident_sin matches 1 run function rpg:inquest/give/pact1
execute if score @s rpg_ident_sin matches 2 run function rpg:inquest/give/pact2
execute if score @s rpg_ident_sin matches 3 run function rpg:inquest/give/pact3
execute if score @s rpg_ident_sin matches 4 run function rpg:inquest/give/pact4
execute if score @s rpg_ident_sin matches 5 run function rpg:inquest/give/pact5
execute if score @s rpg_ident_sin matches 6 run function rpg:inquest/give/pact6
execute if score @s rpg_ident_sin matches 7 run function rpg:inquest/give/pact7
tellraw @s ["",{"text":"[契约]","color":"#D596F2","bold":true,"italic":false},{"text":"　你的领主在你背包里留下了一本契约之书。","color":"#9C9A94","bold":false,"italic":false}]
