# 变成精英（as/at 它）
tag @s add rpg.el
execute store result score @s rpg_el_a1 run random value 1..10
scoreboard players set @s rpg_el_a2 0
execute if score #sef rpg_el matches 6.. store result score #c rpg_el run random value 1..5
execute if score #sef rpg_el matches 6.. if score #c rpg_el matches 1 run function rpg:elite/champion
function rpg:elite/stats
function rpg:elite/type
function rpg:elite/name_pick
execute if score @s rpg_el_a1 matches 1 run function rpg:elite/a/1/on
execute if score @s rpg_el_a2 matches 1 run function rpg:elite/a/1/on
execute if score @s rpg_el_a1 matches 2 run function rpg:elite/a/2/on
execute if score @s rpg_el_a2 matches 2 run function rpg:elite/a/2/on
execute if score @s rpg_el_a1 matches 3 run function rpg:elite/a/3/on
execute if score @s rpg_el_a2 matches 3 run function rpg:elite/a/3/on
execute if score @s rpg_el_a1 matches 4 run function rpg:elite/a/4/on
execute if score @s rpg_el_a2 matches 4 run function rpg:elite/a/4/on
execute if score @s rpg_el_a1 matches 5 run function rpg:elite/a/5/on
execute if score @s rpg_el_a2 matches 5 run function rpg:elite/a/5/on
execute if score @s rpg_el_a1 matches 6 run function rpg:elite/a/6/on
execute if score @s rpg_el_a2 matches 6 run function rpg:elite/a/6/on
execute if score @s rpg_el_a1 matches 7 run function rpg:elite/a/7/on
execute if score @s rpg_el_a2 matches 7 run function rpg:elite/a/7/on
execute if score @s rpg_el_a1 matches 8 run function rpg:elite/a/8/on
execute if score @s rpg_el_a2 matches 8 run function rpg:elite/a/8/on
execute if score @s rpg_el_a1 matches 9 run function rpg:elite/a/9/on
execute if score @s rpg_el_a2 matches 9 run function rpg:elite/a/9/on
execute if score @s rpg_el_a1 matches 10 run function rpg:elite/a/10/on
execute if score @s rpg_el_a2 matches 10 run function rpg:elite/a/10/on
