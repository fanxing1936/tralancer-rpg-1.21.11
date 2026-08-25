# 饥荒。贪婪拿走的不一定是你身上的东西 —— 也可以是你下一顿。
effect give @s minecraft:hunger 8 1 true
function rpg:hud/m28
playsound minecraft:entity.generic.eat player @s ~ ~ ~ 0.8 0.5
