# @s 是稳定占有第 1 槽的 Boss：名称、值与观众来自同一实体。
execute store result bossbar minecraft:devil value run data get entity @s Health
bossbar set minecraft:devil players @a[distance=..20]
execute if entity @s[type=minecraft:evoker] run bossbar set minecraft:devil name {"text":"\ue301\ue302\ue303"}
execute if entity @s[type=minecraft:vindicator,tag=devil2] run bossbar set minecraft:devil name {"text":"\ue201\ue202\ue203"}
