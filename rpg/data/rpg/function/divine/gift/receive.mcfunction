effect clear @s minecraft:blindness
effect clear @s minecraft:darkness
effect clear @s minecraft:wither
effect clear @s minecraft:poison
effect clear @s minecraft:slowness
effect clear @s minecraft:weakness
effect give @s minecraft:instant_health 1 1 true
effect give @s minecraft:regeneration 10 1 true
effect give @s minecraft:absorption 20 1 true
effect give @s minecraft:resistance 8 0 true
particle minecraft:flash{color:16774312} ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:heart ~ ~1.1 ~ 0.55 0.75 0.55 0.12 24 force
particle minecraft:totem_of_undying ~ ~1 ~ 0.65 0.85 0.65 0.08 42 force
playsound minecraft:item.totem.use player @s ~ ~ ~ 0.65 1.35
tellraw @s ["",{"text":"[圣子恩赐] ","color":"#FFF2A8","bold":true,"italic":false},{"text":"他者为你分授生命；伤痕与污秽正在退去。","color":"gray","bold":false,"italic":false}]
