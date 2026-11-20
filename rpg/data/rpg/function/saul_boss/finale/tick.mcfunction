# 死亡（as/at 他）：剑落、跪下、倒地、躺下，在天光里沉入地面、散成白灰，然后结算
scoreboard players add @s rpg_sl_c 1
execute if score @s rpg_sl_c matches 10 run function rpg:saul_boss/finale/drop
execute if score @s rpg_sl_c matches 20 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……好剑。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sl_c matches 44 run function rpg:saul/anim/enter/fall
execute if score @s rpg_sl_c matches 44 run playsound minecraft:entity.player.big_fall hostile @a[distance=..32] ~ ~ ~ 1 0.8
execute if score @s rpg_sl_c matches 68 run function rpg:saul/anim/enter/down
execute if score @s rpg_sl_c matches 70 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"斯塔福德，你终于……赢了我一次。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sl_c matches 1..160 run particle minecraft:dust{color:[0.78,0.78,0.74],scale:0.8} ~ ~1 ~ 0.6 0.6 0.6 0 1
execute if score @s rpg_sl_c matches 90 run function rpg:saul_boss/vfx/fall
execute if score @s rpg_sl_c matches 110 run function rpg:saul_boss/vfx/death
execute if score @s rpg_sl_c matches 110 run tellraw @a[distance=..48] ["",{"text":"〖","color":"#8C96A2","bold":true,"italic":false},{"text":"扫罗","color":"#C9505A","bold":true,"italic":false},{"text":"〗","color":"#8C96A2","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"……老伙计，等等我。","color":"#9C9A94","bold":false,"italic":false}]
execute if score @s rpg_sl_c matches 112..150 run tp @s ~ ~-0.04 ~
execute if score @s rpg_sl_c matches 112..150 run particle minecraft:white_ash ~ ~0.8 ~ 0.6 0.4 0.6 0.02 8
execute if score @s rpg_sl_c matches 112..150 run particle minecraft:dust_color_transition{from_color:[0.95,0.97,1.0],to_color:[0.55,0.6,0.68],scale:1.1} ~ ~0.6 ~ 0.5 0.3 0.5 0 2
execute if score @s rpg_sl_c matches 112..150 run particle minecraft:soul ~ ~0.6 ~ 0.4 0.2 0.4 0.02 1
execute if score @s rpg_sl_c matches 150 run particle minecraft:flash{color:14212838} ~ ~0.5 ~ 0 0 0 0 1 force
execute if score @s rpg_sl_c matches 150 run playsound minecraft:block.amethyst_block.resonate hostile @a[distance=..40] ~ ~ ~ 1.2 0.6
execute if score @s rpg_sl_c matches 156.. run function rpg:saul_boss/victory
