# 9 行原本各自扫一遍全实体表找 @e[tag=bubble]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[tag=bubble] at @s run particle dust_color_transition{from_color:[0.0,0.7,1.0],to_color:[0.56,0.97,1.0],scale:1} ~0.1 ~0.1 ~0.1 -0.2 -0.2 -0.2 0.2 10 force
execute as @e[tag=bubble] at @s run data merge entity @e[limit=1,sort=nearest,distance=0.1..2] {Motion:[0d,2.5d,0d]}
execute as @e[tag=bubble] at @s if entity @e[limit=1,sort=nearest,distance=0.1..1.9,tag=!rpg.h.bubble_tag1] run summon firework_rocket ~ ~1 ~ {Life:1,LifeTime:0,FireworksItem:{id:firework_rocket,components:{fireworks:{explosions:[{shape:burst,has_twinkle:1b,has_trail:1b,colors:[I;3847130,16701501,16762429,1487834],fade_colors:[I;3847130]}]}}}}
execute as @e[tag=bubble] at @s unless block ~ ~-0.1 ~ air run kill @s
execute as @e[tag=bubble] at @s unless block ~ ~0.1 ~ air run kill @s
execute as @e[tag=bubble] at @s unless block ~0.1 ~ ~ air run kill @s
execute as @e[tag=bubble] at @s unless block ~-0.1 ~ ~ air run kill @s
execute as @e[tag=bubble] at @s unless block ~ ~ ~-0.1 air run kill @s
execute as @e[tag=bubble] at @s unless block ~ ~ ~0.1 air run kill @s
