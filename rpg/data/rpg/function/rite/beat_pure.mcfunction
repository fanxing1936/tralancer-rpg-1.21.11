# 净化的节拍：一拍比一拍弱。
execute if entity @s[scores={rpg_totem=200}] run function rpg:rite/p1
execute if entity @s[scores={rpg_totem=160}] run function rpg:rite/p2
execute if entity @s[scores={rpg_totem=120}] run function rpg:rite/p3
execute if entity @s[scores={rpg_totem=80}] run function rpg:rite/p4
execute if entity @s[scores={rpg_totem=40}] run function rpg:rite/p5
particle dust{color:[0.98,0.92,0.62],scale:1} ~ ~0.7 ~ 0.22 0.3 0.22 0.01 2
execute if entity @s[scores={rpg_totem=1..}] run scoreboard players remove @s rpg_totem 1
execute if entity @s[scores={rpg_totem=..0}] run function rpg:rite/burst
