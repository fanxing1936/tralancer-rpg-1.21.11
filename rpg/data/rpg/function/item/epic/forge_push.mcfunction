# 被热浪推开一步，并被点燃。
execute at @s facing entity @p[tag=rpg.h.forge_tag1] feet run tp @s ^ ^ ^-0.7
effect give @s minecraft:fire_resistance 1 0 true
execute at @s run particle minecraft:flash{color:13193984} ~ ~1 ~ 0 0 0 0 1
