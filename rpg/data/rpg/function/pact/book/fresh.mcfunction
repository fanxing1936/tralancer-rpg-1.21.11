# 把手里的书换成当前阶位的样子。
execute if score @s rpg_pact matches 1 run function rpg:pact/book/p1
execute if score @s rpg_pact matches 2 run function rpg:pact/book/p2
execute if score @s rpg_pact matches 3 run function rpg:pact/book/p3
execute if score @s rpg_pact matches 4 run function rpg:pact/book/p4
execute if score @s rpg_pact matches 5 run function rpg:pact/book/p5
execute if score @s rpg_pact matches 6 run function rpg:pact/book/p6
execute if score @s rpg_pact matches 7 run function rpg:pact/book/p7
