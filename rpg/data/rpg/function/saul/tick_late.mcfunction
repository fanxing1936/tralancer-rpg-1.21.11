# 扫罗的身体是模型：载体本身始终隐身（驱魔的显形只清隐身效果，没有逻辑读它）。
execute as @e[tag=rpg.slm] unless predicate rpg:saul/invisible run effect give @s minecraft:invisibility infinite 0 true
