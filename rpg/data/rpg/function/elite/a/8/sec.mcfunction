execute if entity @s[tag=rpg.el.called] run return 0
execute store result score #h rpg_el run data get entity @s Health 10
execute store result score #mh rpg_el run attribute @s minecraft:max_health get 5
execute if score #h rpg_el > #mh rpg_el run return 0
tag @s add rpg.el.called
function rpg:elite/type
function rpg:elite/a/8/call with storage rpg:elite t
function rpg:elite/a/8/call with storage rpg:elite t
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..24] ~ ~ ~ 1 1
particle minecraft:dust{color:[0.64,0.46,0.75],scale:1.4} ~ ~1 ~ 1 0.6 1 0 30
