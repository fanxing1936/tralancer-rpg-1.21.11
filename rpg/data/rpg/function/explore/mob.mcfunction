# 主世界的怪第一次出现（as/at 它）：近郊弱化、不出精英；深处精英多；危险 III–V 的群系加强
tag @s add rpg.ow.s
execute if data entity @s CustomName run return 0
scoreboard players set #lv rpg_xb 1
execute if biome ~ ~ ~ #rpg:ex/desert run scoreboard players set #lv rpg_xb 2
execute if biome ~ ~ ~ #rpg:ex/snowfield run scoreboard players set #lv rpg_xb 2
execute if biome ~ ~ ~ #rpg:ex/taiga run scoreboard players set #lv rpg_xb 2
execute if biome ~ ~ ~ #rpg:ex/mesa run scoreboard players set #lv rpg_xb 3
execute if biome ~ ~ ~ #rpg:ex/eroded run scoreboard players set #lv rpg_xb 3
execute if biome ~ ~ ~ #rpg:ex/ashwood run scoreboard players set #lv rpg_xb 3
execute if biome ~ ~ ~ #rpg:ex/stone run scoreboard players set #lv rpg_xb 3
execute if biome ~ ~ ~ #rpg:ex/warped run scoreboard players set #lv rpg_xb 4
execute if biome ~ ~ ~ #rpg:ex/glacier run scoreboard players set #lv rpg_xb 4
execute if biome ~ ~ ~ #rpg:ex/alpine run scoreboard players set #lv rpg_xb 4
execute if biome ~ ~ ~ #rpg:ex/volcano run scoreboard players set #lv rpg_xb 5
execute if biome ~ ~ ~ #rpg:ex/war run scoreboard players set #lv rpg_xb 5
execute if biome ~ ~ ~ #rpg:ex/cliffs run scoreboard players set #lv rpg_xb 2
execute store result score #mx rpg_xb run data get entity @s Pos[0]
execute store result score #mz rpg_xb run data get entity @s Pos[2]
scoreboard players set #best rpg_xb 2147483647
execute if score #s1 rpg_tw matches 3 run function rpg:explore/d2 {i:1}
execute if score #s2 rpg_tw matches 3 run function rpg:explore/d2 {i:2}
execute if score #s3 rpg_tw matches 3 run function rpg:explore/d2 {i:3}
execute if score #s4 rpg_tw matches 3 run function rpg:explore/d2 {i:4}
execute if score #s5 rpg_tw matches 3 run function rpg:explore/d2 {i:5}
execute if score #s6 rpg_tw matches 3 run function rpg:explore/d2 {i:6}
execute if score #s7 rpg_tw matches 3 run function rpg:explore/d2 {i:7}
execute if score #s8 rpg_tw matches 3 run function rpg:explore/d2 {i:8}
execute if score #s9 rpg_tw matches 3 run function rpg:explore/d2 {i:9}
execute if score #s10 rpg_tw matches 3 run function rpg:explore/d2 {i:10}
execute if score #s11 rpg_tw matches 3 run function rpg:explore/d2 {i:11}
execute if score #s12 rpg_tw matches 3 run function rpg:explore/d2 {i:12}
execute if score #s13 rpg_tw matches 3 run function rpg:explore/d2 {i:13}
execute if score #s14 rpg_tw matches 3 run function rpg:explore/d2 {i:14}
execute if score #s15 rpg_tw matches 3 run function rpg:explore/d2 {i:15}
execute if score #s16 rpg_tw matches 3 run function rpg:explore/d2 {i:16}
execute if score #s17 rpg_tw matches 3 run function rpg:explore/d2 {i:17}
execute if score #s18 rpg_tw matches 3 run function rpg:explore/d2 {i:18}
execute if score #s19 rpg_tw matches 3 run function rpg:explore/d2 {i:19}
execute if score #s20 rpg_tw matches 3 run function rpg:explore/d2 {i:20}
execute if score #best rpg_xb matches ..360000 if score #lv rpg_xb matches ..2 run return run function rpg:explore/weak
execute if score #best rpg_xb matches 4000001.. run tag @s add rpg.ow.deep
execute if score #lv rpg_xb matches 3 run function rpg:explore/lv3
execute if score #lv rpg_xb matches 4 run function rpg:explore/lv4
execute if score #lv rpg_xb matches 5 run function rpg:explore/lv5
