# 宏展开的那一行。$(atk) 是上一步读到的攻击力。
$execute as @e[tag=rpg.sq.mark,limit=1,sort=nearest,distance=..3.4] run damage @s $(atk) minecraft:mob_attack by @e[tag=rpg.sq.striker,limit=1]
