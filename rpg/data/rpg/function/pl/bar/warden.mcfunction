# Gate Warden 的位图血条（as/at 它）
execute store result score #h rpg_el run data get entity @s Health 20
execute store result score #mh rpg_el run attribute @s minecraft:max_health get
scoreboard players operation #h rpg_el /= #mh rpg_el
execute if score #h rpg_el matches 0 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 1 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 2 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 3 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 4 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 5 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 6 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 7 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 8 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 9 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 10 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 11 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 12 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 13 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 14 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 15 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 16 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 17 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 18 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 19 run data modify storage rpg:elite t.st set value ""
execute if score #h rpg_el matches 20 run data modify storage rpg:elite t.st set value ""
data modify storage rpg:elite t.i1 set value ""
data modify storage rpg:elite t.i2 set value ""
data modify storage rpg:elite t.bb set value ""
data modify storage rpg:elite t.bn set value ""
data modify storage rpg:elite t.bo set value ""
function rpg:elite/bar_set with storage rpg:elite t
bossbar set rpg:elite_champion_bar players @a[distance=..32]
