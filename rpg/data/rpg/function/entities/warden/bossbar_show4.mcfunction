# @s 是稳定占有第 4 槽的 Boss：名称、值与观众来自同一实体。
execute store result bossbar minecraft:devil4 value run data get entity @s Health
bossbar set minecraft:devil4 players @a[distance=..20]
execute if entity @s[type=minecraft:evoker] run bossbar set minecraft:devil4 name {"text":"\ue301\ue302\ue303"}
execute if entity @s[type=minecraft:vindicator,tag=devil2] run bossbar set minecraft:devil4 name {"text":"\ue201\ue202\ue203"}
