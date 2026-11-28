execute unless entity @s[tag=rpg.ow.s] if dimension minecraft:overworld run function rpg:explore/mob
execute if entity @s[tag=rpg.ow.weak] run return 0
# 第一次见到这只生物（as/at 它）
tag @s add rpg.el.seen
execute if data entity @s CustomName run return 0
execute if data entity @s {NoAI:1b} run return 0
# 本包召唤的生物都带标签；掉落策略那一枚不算
execute store result score #nt rpg_el run data get entity @s Tags
scoreboard players remove #nt rpg_el 1
execute if entity @s[tag=rpg.drop_policy.v1] run scoreboard players remove #nt rpg_el 1
execute if entity @s[tag=rpg.pl.s] run scoreboard players remove #nt rpg_el 1
execute if entity @s[tag=rpg.pl.z1] run scoreboard players remove #nt rpg_el 1
execute if entity @s[tag=rpg.pl.z2] run scoreboard players remove #nt rpg_el 1
execute if entity @s[tag=rpg.pl.z3] run scoreboard players remove #nt rpg_el 1
execute if score #nt rpg_el matches 1.. run return 0
execute if entity @s[tag=rpg.ow.deep] run scoreboard players operation #p rpg_el *= #2 rpg_el
execute unless entity @a[distance=..64,gamemode=!spectator] run return 0
execute store result score #near rpg_el if entity @e[tag=rpg.el,distance=..48]
execute if score #near rpg_el matches 3.. run return 0
# 千分之 30 + 5 × 原质阶，封顶 80；夜里 ×1.5
scoreboard players set #sef rpg_el 0
execute as @a[distance=..64] if score @s rpg_sef > #sef rpg_el run scoreboard players operation #sef rpg_el = @s rpg_sef
scoreboard players operation #p rpg_el = #sef rpg_el
scoreboard players operation #p rpg_el *= #5 rpg_el
scoreboard players add #p rpg_el 30
execute if score #p rpg_el matches 81.. run scoreboard players set #p rpg_el 80
execute store result score #day rpg_el run time query daytime
execute if score #day rpg_el matches 13000..23000 run scoreboard players operation #p rpg_el *= #3 rpg_el
execute if score #day rpg_el matches 13000..23000 run scoreboard players operation #p rpg_el /= #2 rpg_el
execute if score #tide rpg_ev matches 1 run scoreboard players operation #p rpg_el *= #3 rpg_el
execute if entity @s[tag=rpg.pl.z1] run scoreboard players operation #p rpg_el *= #2 rpg_el
execute if entity @s[tag=rpg.pl.z2] run scoreboard players operation #p rpg_el *= #3 rpg_el
execute if entity @s[tag=rpg.pl.z3] run scoreboard players operation #p rpg_el *= #4 rpg_el
execute if entity @s[tag=rpg.pl.s] if score #moon rpg_pl matches 1.. run scoreboard players operation #p rpg_el *= #2 rpg_el
execute if entity @s[tag=rpg.pl.s] if score #rain rpg_pl matches 1.. run scoreboard players operation #p rpg_el *= #2 rpg_el
execute if entity @s[tag=rpg.pl.s] if score #p rpg_el matches 251.. run scoreboard players set #p rpg_el 250
execute if entity @s[tag=rpg.pl.z2] if score #sef rpg_el matches ..5 run scoreboard players set #sef rpg_el 6
execute if entity @s[tag=rpg.pl.z3] if score #sef rpg_el matches ..5 run scoreboard players set #sef rpg_el 6
execute if entity @a[scores={rpg_po_lu=1..},distance=..48] run scoreboard players operation #p rpg_el *= #3 rpg_el
execute store result score #r rpg_el run random value 1..1000
execute if score #r rpg_el > #p rpg_el run return 0
function rpg:elite/make
