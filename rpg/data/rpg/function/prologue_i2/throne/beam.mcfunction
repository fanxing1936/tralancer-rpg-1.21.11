# 一道圣光（as 被瞄准的玩家，at 座天使）
particle minecraft:flash{color:[1.0,0.9,0.6,1.0]} ~ ~ ~ 0 0 0 0 1
execute facing entity @s eyes run function rpg:prologue_i2/throne/beam_line
damage @s 4 minecraft:magic
playsound minecraft:entity.guardian.attack master @s ~ ~ ~ 1 1.4
