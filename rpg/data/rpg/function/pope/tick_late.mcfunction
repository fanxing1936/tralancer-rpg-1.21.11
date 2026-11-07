# 参照亚巴顿：在 command/tick_end 之后恢复载体隐身，不改显形/受伤逻辑。
execute in minecraft:overworld as @e[distance=0..,type=minecraft:vindicator,tag=rpg.pope] unless predicate rpg:pope/invisible run effect give @s minecraft:invisibility infinite 0 true
execute in minecraft:the_nether as @e[distance=0..,type=minecraft:vindicator,tag=rpg.pope] unless predicate rpg:pope/invisible run effect give @s minecraft:invisibility infinite 0 true
execute in minecraft:the_end as @e[distance=0..,type=minecraft:vindicator,tag=rpg.pope] unless predicate rpg:pope/invisible run effect give @s minecraft:invisibility infinite 0 true
