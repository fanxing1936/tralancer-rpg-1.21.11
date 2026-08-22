# 每个被缠住的目标：拽近一步、钉住、挂上六鞭的计数
scoreboard players set @s rpg_vine_lash 60
tag @s add rpg.vine.lash
effect give @s minecraft:slowness 4 3 true
execute if entity @a[tag=rpg.vine.src,distance=1.6..8] facing entity @a[tag=rpg.vine.src,limit=1,sort=nearest] feet run tp @s ^ ^ ^1.6
particle minecraft:tinted_leaves{color:12835692} ~ ~1 ~ 0.4 0.5 0.4 0.02 20
