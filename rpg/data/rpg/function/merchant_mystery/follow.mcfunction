# 骑乘负责位移，模型部件同步当前村民朝向。
execute on passengers if entity @s[type=minecraft:item_display,tag=rpg.mer.model.mystery.part] run rotate @s ~ 0
function rpg:merchant_mystery/anim/tick
execute unless predicate rpg:merchant_mystery/invisible run effect give @s minecraft:invisibility infinite 0 true
