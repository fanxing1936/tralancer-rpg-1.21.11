# 死亡（as/at 他）：肋骨落下、跪下、倒地，一层层变淡、散成白光，然后结算
scoreboard players add @s rpg_mk_c 1
execute if score @s rpg_mk_c matches 8 run function rpg:michael_boss_i4/finale/drop
execute if score @s rpg_mk_c matches 30 run execute unless score #pro rpg_mk_i4 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_mk_c matches 44 run function rpg:michael/anim/enter/fall
execute if score @s rpg_mk_c matches 68 run function rpg:michael/anim/enter/down
execute if score @s rpg_mk_c matches 70 run execute unless score #pro rpg_mk_i4 matches 1 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#FF805F","bold":true,"italic":false},{"text":"炽天使 ","color":"#FF805F","bold":true,"italic":false},{"text":"米迦勒","color":"#FF3300","bold":true,"italic":false},{"text":"〗","color":"#FF805F","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……主责备你吧。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_mk_c matches 76 run function rpg:michael_boss_i4/vfx/death/halo
execute if score @s rpg_mk_c matches 78 run function rpg:michael/wings/burn/1
execute if score @s rpg_mk_c matches 82 run function rpg:michael/wings/burn/2
execute if score @s rpg_mk_c matches 86 run function rpg:michael/wings/burn/3
execute if score @s rpg_mk_c matches 90 run function rpg:michael/wings/burn/4
execute if score @s rpg_mk_c matches 94 run function rpg:michael/wings/burn/5
execute if score @s rpg_mk_c matches 98 run function rpg:michael/wings/burn/6
execute if score @s rpg_mk_c matches 78 run function rpg:michael_boss_i4/vfx/death/wing
execute if score @s rpg_mk_c matches 82 run function rpg:michael_boss_i4/vfx/death/wing
execute if score @s rpg_mk_c matches 86 run function rpg:michael_boss_i4/vfx/death/wing
execute if score @s rpg_mk_c matches 90 run function rpg:michael_boss_i4/vfx/death/wing
execute if score @s rpg_mk_c matches 94 run function rpg:michael_boss_i4/vfx/death/wing
execute if score @s rpg_mk_c matches 98 run function rpg:michael_boss_i4/vfx/death/wing
execute if score @s rpg_mk_c matches 100 run function rpg:michael/look/fade
execute if score @s rpg_mk_c matches 70..130 run particle minecraft:end_rod ~ ~0.8 ~ 0.6 0.4 0.6 0.02 2
execute if score @s rpg_mk_c matches 100..130 run particle minecraft:white_ash ~ ~0.8 ~ 0.7 0.4 0.7 0.02 6
execute if score @s rpg_mk_c matches 108 run function rpg:michael_boss_i4/vfx/death/gather
execute if score @s rpg_mk_c matches 124 run function rpg:michael_boss_i4/vfx/death
execute if score @s rpg_mk_c matches 124 run title @a[distance=..48] times 0 3 0
execute if score @s rpg_mk_c matches 124 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score @s rpg_mk_c matches 126 run title @a[distance=..48] times 0 3 0
execute if score @s rpg_mk_c matches 126 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score @s rpg_mk_c matches 128 run title @a[distance=..48] times 0 3 0
execute if score @s rpg_mk_c matches 128 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score @s rpg_mk_c matches 130 run title @a[distance=..48] times 0 2 14
execute if score @s rpg_mk_c matches 130 run title @a[distance=..48] title {"text": "", "font": "rpg:michael_vfx", "color": "white"}
execute if score @s rpg_mk_c matches 128 run execute on passengers run kill @s
execute if score @s rpg_mk_c matches 136 run function rpg:michael_boss_i4/vfx/death/after
execute if score @s rpg_mk_c matches 130..190 run particle minecraft:end_rod ~ ~6 ~ 2.5 1.5 2.5 0 1
execute if score @s rpg_mk_c matches 200.. run function rpg:michael_boss_i4/victory
