scoreboard players add @s rpg_jq_c 1
execute if score @s rpg_jq_c matches 24 run function rpg:jacques/anim/enter/down
execute if score @s rpg_jq_c matches 1..40 run particle minecraft:large_smoke ~ ~0.6 ~ 0.6 0.3 0.6 0.02 3
execute if score @s rpg_jq_c matches 1..20 run particle minecraft:flame ~ ~0.5 ~ 0.6 0.3 0.6 0.01 2
execute if score @s rpg_jq_c matches 1 run function rpg:jacques_boss/vfx/fall
execute if score @s rpg_jq_c matches 20..120 run particle minecraft:dust_color_transition{from_color:[1.0,0.62,0.2],to_color:[0.35,0.04,0.0],scale:1.4} ~ ~0.6 ~ 0.6 0.4 0.6 0 1
execute if score @s rpg_jq_c matches 20..120 run particle minecraft:white_ash ~ ~1.5 ~ 1 1 1 0.01 3
execute if score @s rpg_jq_c matches 60 as @e[type=minecraft:vindicator,tag=rpg.jqd] at @s run function rpg:jacques_boss/vfx/david_hero
execute if score @s rpg_jq_c matches 40 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#C8102E","bold":true,"italic":false},{"text":"雅克","color":"#FF8A3D","bold":true,"italic":false},{"text":"〗","color":"#C8102E","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……我守了一辈子的，是谁？","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_jq_c matches 60 as @e[type=minecraft:vindicator,tag=rpg.jqd] at @s run function rpg:david/anim/enter/hero
execute if score @s rpg_jq_c matches 140.. run function rpg:jacques_boss/victory
